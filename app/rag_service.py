import os
import requests
from dotenv import load_dotenv
from app.document_loader import load_document, Document
from app.vector_store import store_chunks, get_vector_db
from app.embedding_service import get_embeddings

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")


def split_text(text, chunk_size=500, chunk_overlap=50):
    chunks = []
    if not text:
        return chunks
    
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start += chunk_size - chunk_overlap
    return chunks


def process_document(filename, content):
    documents = load_document(filename, content)

    all_chunks = []
    for doc in documents:
        chunks = split_text(doc.page_content, chunk_size=500, chunk_overlap=50)
        for chunk_text in chunks:
            all_chunks.append(Document(page_content=chunk_text, metadata=doc.metadata))

    store_chunks(all_chunks)

    return len(all_chunks)


def ask_llm(question, context):

    url = "https://integrate.api.nvidia.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Context:
{context}

Question:
{question}

Answer using only the context above.
"""

    payload = {
        "model": "meta/llama3-70b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 500
    }

    response = requests.post(url, headers=headers, json=payload)

    result = response.json()

    return result["choices"][0]["message"]["content"]


def ask_question(question):

    collection = get_vector_db()
    model = get_embeddings()

    if collection is None:
        return "No document uploaded."

    query_embedding = model.encode([question])

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    if not results["documents"] or not results["documents"][0]:
        return "No relevant context found."

    context = "\n".join(results["documents"][0])

    answer = ask_llm(question, context)

    return answer