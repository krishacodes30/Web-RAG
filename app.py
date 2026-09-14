import streamlit as st
from ingest import ingest_url
from query import answer_question

st.set_page_config(page_title="Website RAG", layout="wide")
st.title("🔎 Website RAG — LangChain + Ollama + pgvector")

st.subheader("1. Add a website to the knowledge base")
url = st.text_input("Website URL")
if st.button("Scrape & Index") and url:
    with st.spinner("Scraping, chunking, embedding, storing..."):
        num_chunks = ingest_url(url)
    st.success(f"Indexed {num_chunks} chunks from {url}")

st.subheader("2. Ask a question")
question = st.text_input("Your question")
if question:
    with st.spinner("Retrieving relevant chunks + generating answer..."):
        result = answer_question(question)

    st.write("### Answer")
    st.write(result["answer"])

    with st.expander("Retrieved source chunks (why it answered this way)"):
        for i, doc in enumerate(result["sources"], 1):
            st.markdown(f"**Chunk {i}** — from `{doc.metadata.get('source', 'unknown')}`")
            st.write(doc.page_content[:400])
            st.divider()