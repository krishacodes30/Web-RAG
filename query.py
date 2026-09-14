from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_postgres import PGVector

import config

def get_vectorstore():
    embeddings = OllamaEmbeddings(model=config.EMBED_MODEL, base_url=config.OLLAMA_HOST)
    return PGVector(
        embeddings=embeddings,
        collection_name=config.COLLECTION_NAME,
        connection=config.CONNECTION_STRING,
        use_jsonb=True,
    )

def answer_question(question: str, k: int = 4) -> dict:
    vectorstore = get_vectorstore()

    # RETRIEVE: find the k most semantically similar chunks to the question
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    relevant_docs = retriever.invoke(question)

    # Combine retrieved chunks into one context block for the prompt
    context = "\n\n".join(doc.page_content for doc in relevant_docs)

    # AUGMENT + GENERATE: build the prompt and call the LLM
    llm = ChatOllama(model=config.LLM_MODEL, base_url=config.OLLAMA_HOST, temperature=0)
    prompt = (
        f"Answer the question using ONLY the context below. "
        f"If the answer isn't in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}"
    )
    response = llm.invoke(prompt)

    return {"answer": response.content, "sources": relevant_docs}