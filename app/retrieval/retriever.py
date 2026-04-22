from app.retrieval.vector_store import load_index
from app.retrieval.reranker import rerank

def retrieve(repo_id, query):
    db = load_index(repo_id)
    if not db:
        return []

    docs = db.similarity_search(query, k=15)
    return rerank(query, docs)