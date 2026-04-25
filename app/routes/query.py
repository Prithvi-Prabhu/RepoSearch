from fastapi import APIRouter, Request
from app.utils.helpers import get_repo_id
from app.core.config import MAX_QUERY_LENGTH
from app.core.rate_limiter import limiter
from app.core.security import sanitize_query, validate_repo_url

router = APIRouter()

@router.get("/query")
@limiter.limit("10/minute")
def query(request: Request, repo_url: str, q: str):

    from app.chains.rag_chain import run  
    if len(q) > MAX_QUERY_LENGTH:
        return {"error": f"Query too long (max {MAX_QUERY_LENGTH} characters)"}

    repo_url = validate_repo_url(repo_url)
    q = sanitize_query(q)

    repo_id = get_repo_id(repo_url)
    answer, sources = run(repo_id, q)

    return {"answer": answer, "sources": sources}
