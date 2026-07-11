import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings
from app.database import Base, engine
from app.middleware.logging_middleware import log_requests
from app.routers import auth, notices, placement

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    logging.info("Database tables verified/created")
    yield
    logging.info("Shutting down CampusHub API")


app = FastAPI(
    title=settings.APP_NAME,
    description="A Smart Student Productivity Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow configured origins + localhost for dev
allowed_origins = [
    "http://localhost:5173",
    settings.FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

app.include_router(auth.router)
app.include_router(notices.router)
app.include_router(placement.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}
