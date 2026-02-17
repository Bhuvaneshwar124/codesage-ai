from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import EMBEDDING_MODEL, TOP_K, VECTOR_STORE_DIR


def load_vector_store():
    """Load the persisted FAISS vector store from disk."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return FAISS.load_local(
        str(VECTOR_STORE_DIR), embeddings, allow_dangerous_deserialization=True
    )


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    """Retrieve the most relevant document chunks for a given query.

    Returns a list of dicts with 'content' and 'metadata' keys.
    """
    store = load_vector_store()
    results = store.similarity_search(query, k=top_k)
    return [
        {"content": doc.page_content, "metadata": doc.metadata}
        for doc in results
    ]
