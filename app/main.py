from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import lifespan
from app.api.v1.router import router

app = FastAPI(
    title="FintrackPro Backend",
    description="Financial management backend API built with FastAPI and MongoDB Atlas.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
