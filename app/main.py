from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import init_db
from app.routers import customers, jobs


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Construction Estimate & Management API", version="0.1.0", lifespan=lifespan)
app.include_router(customers.router)
app.include_router(jobs.router)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}
