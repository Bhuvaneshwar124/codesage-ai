from utils.chunking import chunk_text


def test_chunk_text_basic():
    text = "a" * 1000
    chunks = chunk_text(text, source="test.py", chunk_size=500, chunk_overlap=50)
    assert len(chunks) >= 2
    assert all(c["source"] == "test.py" for c in chunks)


def test_chunk_text_empty():
    chunks = chunk_text("", source="empty.py")
    assert chunks == []


def test_chunk_text_overlap():
    text = "abcdefghij" * 100  # 1000 chars
    chunks = chunk_text(text, source="test.py", chunk_size=500, chunk_overlap=100)
    # With overlap, chunk 1 ends at 500, chunk 2 starts at 400
    assert chunks[1]["text"][:100] == chunks[0]["text"][400:500]


def test_chunk_text_code_aware():
    """Code files should split on function/class boundaries."""
    code = (
        "class Foo:\n"
        "    x = 1\n\n"
        "def bar():\n"
        "    return 2\n\n"
        "def baz():\n"
        "    return 3\n"
    )
    chunks = chunk_text(code, source="module.py", chunk_size=30, chunk_overlap=5)
    assert all(c["metadata"]["file_type"] == "code" for c in chunks)
    assert len(chunks) >= 1


def test_chunk_text_markdown_aware():
    """Markdown files should include file_type metadata."""
    md = "# Title\n\nSome text.\n\n## Section 2\n\nMore text.\n"
    chunks = chunk_text(md, source="README.md", chunk_size=30, chunk_overlap=5)
    assert all(c["metadata"]["file_type"] == "markdown" for c in chunks)


def test_chunk_text_metadata_present():
    """All chunks should carry metadata dict."""
    text = "hello world " * 50
    chunks = chunk_text(text, source="notes.txt")
    assert all("metadata" in c for c in chunks)
    assert all(isinstance(c["metadata"], dict) for c in chunks)

