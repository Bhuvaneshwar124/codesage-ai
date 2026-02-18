from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from config import settings
from services.database import get_db
from sqlalchemy import text
from services.embedding import generate_embedding

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

@app.get("/")
def root():
    return {"message": "RAG Backend Running"}


@app.get("/db-test")
def test_db(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).fetchone()
    return {"database_response": result[0]}

@app.get("/embed-test")
def embed_test():
    embedding = generate_embedding("Hello world")
    return {"embedding_length": len(embedding)}
