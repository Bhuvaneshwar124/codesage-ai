from services.database import search_hybrid, search_similar
from services.embedding import embed_text


async def retrieve(
    query: str, top_k: int = 5, mode: str = "semantic"
) -> list[dict]:
    """Embed the query and perform similarity search against the vector store.

    mode='semantic'  — pure cosine similarity (default)
    mode='hybrid'    — weighted blend of semantic + full-text keyword search
    """
    query_vector = embed_text(query)
    if mode == "hybrid":
        return await search_hybrid(query, query_vector, top_k)
    return await search_similar(query_vector, top_k)
