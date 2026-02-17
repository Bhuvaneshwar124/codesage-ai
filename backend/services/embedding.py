from sentence_transformers import SentenceTransformer

from config import settings

_model = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model


def embed_text(text: str) -> list[float]:
    """Embed a single text string."""
    model = _get_model()
    return model.encode(text, normalize_embeddings=True).tolist()


def embed_chunks(texts: list[str]) -> list[list[float]]:
    """Embed a batch of text strings."""
    model = _get_model()
    embeddings = model.encode(texts, normalize_embeddings=True, batch_size=64)
    return embeddings.tolist()
