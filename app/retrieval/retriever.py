from app.retrieval.vector_store import load_index, similarity_search


def retrieve(repo_id: str, query: str, k: int = 5) -> list[dict]:
    """
    Loads the collection for the given repo and returns the top-k
    most similar chunks as plain dicts {page_content, metadata}.
    Returns an empty list if the repo has not been indexed yet.
    """
    collection = load_index(repo_id)
    if collection is None:
        return []
    return similarity_search(collection, query, k=k)