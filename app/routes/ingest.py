from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.core.security import validate_repo_url
from app.utils.helpers import get_repo_id
from app.ingestion.github_loader import clone_repo
from app.ingestion.file_filter import get_files
from app.ingestion.chunker import chunk_file
from app.retrieval.vector_store import create_index
from app.db.models import repo_exists, insert_repo
from app.core.rate_limiter import limiter

router = APIRouter()

class RepoRequest(BaseModel):
    repo_url: str

@router.post("/ingest")
@limiter.limit("10/minute")
def ingest(request: Request, body: RepoRequest):
    validate_repo_url(body.repo_url)

    repo_id = get_repo_id(body.repo_url)

    if repo_exists(repo_id):
        return {"status": "already indexed"}

    path = clone_repo(body.repo_url, repo_id)

    files = get_files(path)
    docs = []

    for f in files:
        docs.extend(chunk_file(f))

    create_index(docs, repo_id)
    insert_repo(repo_id, body.repo_url)

    return {"status": "indexed", "files": len(files)}