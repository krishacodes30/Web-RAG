# 🔎 Website RAG — Local LLM-Powered Website Q&A

A Retrieval-Augmented Generation (RAG) application that scrapes any website, indexes its content into a vector database, and lets you ask natural-language questions about it — answered by a locally-running LLM (no API keys, no cloud LLM costs).

Built with **LangChain**, **Ollama**, **pgvector (Postgres)**, and **Streamlit**, fully containerized with **Docker**.

---

## ✨ Features

- 🌐 Scrape any public webpage as a knowledge source
- ✂️ Automatic text chunking for accurate retrieval
- 🧠 Local embeddings + local LLM generation via Ollama (fully private, no external API calls)
- 🐘 Persistent vector storage using Postgres + pgvector (survives restarts — no re-scraping)
- 💬 Simple Streamlit chat-style UI
- 🐳 One-command Docker deployment

---

## 🏗️ Architecture

```mermaid
flowchart TD
    U[User Browser] -->|http://localhost:8501| S[Streamlit App]

    subgraph App Container
        S --> I[ingest.py]
        S --> Q[query.py]
    end

    I -->|1. Load page| W[WebBaseLoader]
    W -->|2. Split into chunks| T[Text Splitter]
    T -->|3. Embed chunks| OE[Ollama - nomic-embed-text]
    OE -->|4. Store vectors| PG[(Postgres + pgvector)]

    Q -->|5. Embed question| OE
    Q -->|6. Similarity search| PG
    PG -->|7. Top-k relevant chunks| Q
    Q -->|8. Prompt + context| OL[Ollama - llama3.2]
    OL -->|9. Generated answer| S
```

**Flow explained:**
1. User pastes a URL into the UI → `ingest.py` scrapes it and splits it into overlapping text chunks.
2. Each chunk is turned into a vector embedding by Ollama's `nomic-embed-text` model.
3. Chunks + their vectors are stored in Postgres (via the `pgvector` extension).
4. When the user asks a question, it's embedded the same way, and Postgres finds the most semantically similar chunks (cosine similarity search).
5. Those chunks are stuffed into a prompt as "context," sent to `llama3.2` running in Ollama, and the generated answer is shown in the UI along with its source chunks.

---

## 🧰 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| UI | Streamlit | Simple web interface, no frontend code needed |
| Orchestration | LangChain | Standardized interfaces for loading, splitting, embedding, retrieval, generation |
| Embeddings | Ollama (`nomic-embed-text`) | Converts text → vectors, runs fully local |
| LLM | Ollama (`llama3.2`) | Generates answers grounded in retrieved context |
| Vector Store | Postgres + `pgvector` | Persistent, SQL-queryable vector similarity search |
| Scraping | BeautifulSoup (via LangChain's `WebBaseLoader`) | Extracts clean text from web pages |
| Containerization | Docker + Docker Compose | Reproducible multi-service deployment |

---

## 📁 Project Structure

```
website-rag/
├── app.py              # Streamlit UI — entry point
├── ingest.py           # Scrape → chunk → embed → store pipeline
├── query.py            # Retrieve → generate pipeline
├── config.py            # Central config (model names, connection strings)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Configuration

All settings live in `config.py`:

```python
OLLAMA_HOST = "http://ollama:11434"
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2"
CONNECTION_STRING = "postgresql+psycopg://postgres:password@postgres:5432/ragdb"
COLLECTION_NAME = "website_docs"
```

> For production, move secrets (DB password, etc.) into environment variables rather than hardcoding them.

---

## 🚀 Getting Started (Local, via Docker)

**Prerequisites:** Docker + Docker Compose installed.

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd website-rag

# 2. Start all services (Ollama, Postgres, App)
docker compose up -d

# 3. Pull the required models into the Ollama container
docker exec -it ollama ollama pull nomic-embed-text
docker exec -it ollama ollama pull llama3.2

# 4. Open the app
# http://localhost:8501
```

**Usage:**
1. Paste a website URL → click **Scrape & Index**
2. Type a question about that site → get an answer with source chunks shown below it

---

## 📄 License

MIT — free to use and modify.
