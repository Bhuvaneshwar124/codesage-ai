from services.embedding import embed_text, embed_chunks


def test_embed_text_returns_list():
    result = embed_text("Hello world")
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(v, float) for v in result)


def test_embed_chunks_batch():
    texts = ["first chunk", "second chunk", "third chunk"]
    results = embed_chunks(texts)
    assert len(results) == 3
    assert all(len(r) == len(results[0]) for r in results)


def test_embedding_dimension():
    result = embed_text("dimension check")
    # all-MiniLM-L6-v2 produces 384-dim embeddings
    assert len(result) == 384
