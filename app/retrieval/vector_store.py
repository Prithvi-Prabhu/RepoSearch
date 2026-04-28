import os
import chromadb
from app.core.config import BASE_INDEX_PATH

_embed_model = None


def _get_embed_model():
    global _embed_model
    if _embed_model is None:
        from fastembed import TextEmbedding
        _embed_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    return _embed_model


def _embed(texts: list[str]) -> list[list[float]]:
    model = _get_embed_model()
    return [v.tolist() for v in model.embed(texts)]


def _get_client(repo_id: str) -> chromadb.PersistentClient:
    path = os.path.join(BASE_INDEX_PATH, repo_id)
    os.makedirs(path, exist_ok=True)
    return chromadb.PersistentClient(path=path)


def create_index(docs: list[dict], repo_id: str) -> None:
    client = _get_client(repo_id)

    try:
        client.delete_collection("repo")
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name="repo",
        metadata={"hnsw:space": "cosine"},
    )

    texts     = [d["page_content"] for d in docs]
    metadatas = [d["metadata"]     for d in docs]
    ids       = [str(i)            for i in range(len(docs))]
    embeddings = _embed(texts)

    BATCH = 5000
    for start in range(0, len(docs), BATCH):
        end = start + BATCH
        collection.add(
            ids=ids[start:end],
            embeddings=embeddings[start:end],
            documents=texts[start:end],
            metadatas=metadatas[start:end],
        )


def load_index(repo_id: str):
    path = os.path.join(BASE_INDEX_PATH, repo_id)
    if not os.path.exists(path):
        return None
    try:
        client = chromadb.PersistentClient(path=path)
        return client.get_collection("repo")
    except Exception:
        return None


def similarity_search(collection, query: str, k: int = 5) -> list[dict]:
    query_embedding = _embed([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas"],
    )

    docs = []
    for text, meta in zip(results["documents"][0], results["metadatas"][0]):
        docs.append({"page_content": text, "metadata": meta or {}})
    return docs