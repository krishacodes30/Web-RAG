from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

import config

def ingest_url(url: str) -> int:
    # 1. LOAD: fetch the page and strip it down to text
    loader = WebBaseLoader(web_path=url)
    docs = loader.load()

    # 2. SPLIT: break into small overlapping chunks so embeddings stay focused
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    # 3. EMBED: convert each chunk into a vector using Ollama's embedding model
    embeddings = OllamaEmbeddings(model=config.EMBED_MODEL, base_url=config.OLLAMA_HOST)

    # 4. STORE: push chunks + their vectors into Postgres (pgvector table)
    PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=config.COLLECTION_NAME,
        connection=config.CONNECTION_STRING,
        use_jsonb=True,
    )

    return len(chunks)