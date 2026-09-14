# OLLAMA_HOST = "http://ollama:11434"
# EMBED_MODEL = "nomic-embed-text"     # turns text into vectors
# LLM_MODEL = "llama3.2"               # generates the final answer

# # Postgres connection string LangChain's PGVector needs
# CONNECTION_STRING = "postgresql+psycopg://postgres:password@postgres:5432/ragdb"
# COLLECTION_NAME = "website_docs"     # like a "table namespace" for this project's vectors

OLLAMA_HOST = "http://ollama:11434"
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2:1b"  # Reduced from 3b to 1b model to cut footprint & RAM

CONNECTION_STRING = "postgresql+psycopg://postgres:krisha@postgres:5432/ragdb"
COLLECTION_NAME = "website_docs"