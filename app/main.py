from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from app.routes import ingest, query, eval
from app.core.rate_limiter import limiter

app = FastAPI(
    title="RepoSearch API",
    description="RAG-based assistant for querying GitHub repositories",
    version="1.0.0",
)

# ─── Rate limiter ─────────────────────────────────────────────────────────────
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Rate limit exceeded. Please wait before retrying."},
    )

# ─── CORS (tighten origins in production) ────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Replace with your Streamlit Cloud URL in prod
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ─── Routes ───────────────────────────────────────────────────────────────────
app.include_router(ingest.router)
app.include_router(query.router)
app.include_router(eval.router)

@app.get("/health")
def health():
    return {"status": "ok"}