import chromadb
from app.embedding_service import get_embeddings
import uuid

client = chromadb.EphemeralClient()
collection = client.get_or_create_collection(name="documents")


def store_chunks(chunks):
    model = get_embeddings()

    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]
    ids = [str(uuid.uuid4()) for _ in range(len(chunks))]

    embeddings = model.encode(texts)

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    return collection


def get_vector_db():
    return collection