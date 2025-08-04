import chromadb
from chromadb import PersistentClient
from config import settings


chroma_client = PersistentClient(path=settings.CHROMA_DB_DIR)
collection = chroma_client.get_or_create_collection(name="notes")


def index_note(id: str, text: str, metadata: dict = {}):
    collection.upsert(
        documents=[text],
        ids=[id],
        metadatas=[metadata]
    )

def delete_note(id: str):
    collection.delete(ids=[id])

def search(query: str, k: int = 10):
    result = collection.query(query_texts=[query], n_results=k)
    return [
        {"id": id, "score": dist}
        for id, dist in zip(result["ids"][0], result["distances"][0])
    ]