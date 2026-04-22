from fastapi import APIRouter, Request
from app.chains.rag_chain import run
from app.utils.helpers import get_repo_id
from app.core.config import MAX_QUERY_LENGTH
from app.core.rate_limiter import limiter

router = APIRouter()

@router.get("/query")
@limiter.limit("10/minute")
def query(request: Request, repo_url: str, q: str):
    if len(q) > MAX_QUERY_LENGTH:
        return {"error": "Query too long"}

    repo_id = get_repo_id(repo_url)
    answer, sources = run(repo_id, q)

    return {"answer": answer, "sources": sources}