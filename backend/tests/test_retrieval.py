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
