from services.database import search_similar
from services.embedding import embed_text


async def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """Embed the query and perform similarity search against the vector store."""
    query_vector = embed_text(query)
    return await search_similar(query_vector, top_k)
