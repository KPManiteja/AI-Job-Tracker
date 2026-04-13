from fastapi import FastAPI
from app.api.v1.routes_auth import router as auth_router
from contextlib import asynccontextmanager
from app.core.database import engine, Base
from app.api.v1.routes_jobs import router as jobs_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="AI Job Tracker API")

app.include_router(auth_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "job-tracker"}