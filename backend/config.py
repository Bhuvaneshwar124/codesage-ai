from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://codesage:changeme@localhost:5432/codesage"

    # Embedding
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIM: int = 384  # dimension for all-MiniLM-L6-v2

    # LLM
    LLM_MODEL: str = "mistral"
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    # Chunking
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50

    # Retrieval
    TOP_K: int = 5

    # Uploads
    UPLOAD_DIR: str = str(Path(__file__).resolve().parent.parent / "uploads")

    # Supported file extensions
    SUPPORTED_EXTENSIONS: set[str] = {
        ".py", ".js", ".ts", ".jsx", ".tsx",
        ".java", ".cpp", ".c", ".go", ".rs",
        ".txt", ".md", ".json", ".yaml", ".yml",
        ".toml", ".cfg", ".ini",
        ".html", ".css", ".xml", ".sql",
    }

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
