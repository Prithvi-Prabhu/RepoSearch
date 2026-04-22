from fastapi import FastAPI
from app.routes import ingest, query, eval
from app.core.rate_limiter import limiter

app = FastAPI()
app.state.limiter = limiter

app.include_router(ingest.router)
app.include_router(query.router)
app.include_router(eval.router)