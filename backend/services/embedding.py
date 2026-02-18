import requests
from config import settings


def generate_embedding(text: str):
    print("OLLAMA URL:", settings.OLLAMA_BASE_URL)

    response = requests.post(
        f"{settings.OLLAMA_BASE_URL}/api/embeddings",
        json={
            "model": settings.MODEL_NAME,
            "prompt": text
        }
    )

    response.raise_for_status()

    return response.json()["embedding"]
