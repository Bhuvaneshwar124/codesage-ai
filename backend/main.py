import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import documents, health, ingest, query
from services.database import close_db, init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger("codesage")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting CodeSage AI...")
    await init_db()
    logger.info("Database connected.")
    yield
    await close_db()
    logger.info("CodeSage AI shut down.")


app = FastAPI(
    title="CodeSage AI",
    description="RAG-powered codebase and document analysis API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(ingest.router, prefix="/api")
app.include_router(query.router, prefix="/api")
app.include_router(documents.router, prefix="/api")
