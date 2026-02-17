from langchain_community.llms import Ollama

from config import LLM_MODEL, OLLAMA_BASE_URL

SYSTEM_PROMPT = (
    "You are CodeSage, an expert AI assistant for understanding codebases and "
    "technical documents. Answer the user's question using ONLY the provided context. "
    "If the context does not contain enough information, say so clearly."
)


def build_prompt(query: str, context_chunks: list[dict]) -> str:
    """Construct the augmented prompt from retrieved context and the user query."""
    context_block = "\n\n---\n\n".join(
        f"Source: {chunk['metadata'].get('source', 'unknown')}\n{chunk['content']}"
        for chunk in context_chunks
    )
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"### Context\n{context_block}\n\n"
        f"### Question\n{query}\n\n"
        f"### Answer\n"
    )


def generate(query: str, context_chunks: list[dict]) -> str:
    """Generate an answer using the LLM with retrieved context."""
    prompt = build_prompt(query, context_chunks)
    llm = Ollama(model=LLM_MODEL, base_url=OLLAMA_BASE_URL)
    return llm.invoke(prompt)
