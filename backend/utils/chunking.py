import re

from config import settings

# File extensions treated as code
_CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".java", ".cpp", ".c", ".go", ".rs", ".cs",
    ".rb", ".php", ".swift", ".kt",
}

# Code-aware separators in priority order (try to split on logical boundaries)
_CODE_SEPARATORS = [
    r"\n(?=class )",       # Python/JS class definitions
    r"\n(?=def )",         # Python function definitions
    r"\n(?=async def )",   # Python async functions
    r"\n(?=function )",    # JS/TS functions
    r"\n(?=const |let |var )",  # JS variable declarations
    r"\n\n",               # Blank lines
    r"\n",                 # Any newline
]

_MARKDOWN_SEPARATORS = [
    r"\n#{1,6} ",          # Markdown headings
    r"\n\n",               # Blank lines
    r"\n",                 # Any newline
]


def _split_on_separators(
    text: str, separators: list[str], chunk_size: int
) -> list[str]:
    """Split text using a priority list of regex separators."""
    segments: list[str] = []
    remaining = text

    for sep in separators:
        parts = re.split(sep, remaining)
        current = ""
        for part in parts:
            if len(current) + len(part) <= chunk_size:
                current += part
            else:
                if current.strip():
                    segments.append(current)
                current = part
        if current.strip():
            segments.append(current)
        if len(segments) > 1:
            return segments
        # Not enough splits; reset and try the next separator
        segments = []
        remaining = text

    # Fall back: keep whole text as one segment
    return [text]


def chunk_text(
    text: str,
    source: str = "unknown",
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[dict]:
    """Split text into overlapping chunks with metadata.

    Uses code-aware separators for code files and markdown-aware separators
    for .md files; falls back to character-level splitting for other formats.

    Returns a list of dicts with 'text', 'source', and 'metadata' keys.
    """
    size = chunk_size or settings.CHUNK_SIZE
    overlap = chunk_overlap or settings.CHUNK_OVERLAP

    if not text.strip():
        return []

    # Choose separator strategy based on file extension
    ext = "." + source.rsplit(".", 1)[-1].lower() if "." in source else ""
    if ext in _CODE_EXTENSIONS:
        file_type = "code"
        segments = _split_on_separators(text, _CODE_SEPARATORS, size)
    elif ext == ".md":
        file_type = "markdown"
        segments = _split_on_separators(text, _MARKDOWN_SEPARATORS, size)
    else:
        file_type = "text"
        segments = None  # Use character-level splitting below

    chunks: list[dict] = []

    if segments is not None and len(segments) > 1:
        # Re-combine segments into size-bounded chunks with overlap
        buffer = ""
        for seg in segments:
            if len(buffer) + len(seg) <= size:
                buffer += seg
            else:
                if buffer.strip():
                    chunks.append({
                        "text": buffer,
                        "source": source,
                        "metadata": {"file_type": file_type},
                    })
                # Start new buffer with overlap
                buffer = buffer[max(0, len(buffer) - overlap):] + seg
        if buffer.strip():
            chunks.append({
                "text": buffer,
                "source": source,
                "metadata": {"file_type": file_type},
            })
    else:
        # Character-level sliding window
        start = 0
        while start < len(text):
            end = start + size
            chunk = text[start:end]
            if chunk.strip():
                chunks.append({
                    "text": chunk,
                    "source": source,
                    "metadata": {"file_type": file_type},
                })
            start += size - overlap

    return chunks

