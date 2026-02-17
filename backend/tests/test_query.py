from unittest.mock import AsyncMock, patch

import pytest

from models.schemas import QueryRequest


@pytest.fixture
def query_request():
    return QueryRequest(question="What does main.py do?", top_k=3)


@pytest.mark.asyncio
async def test_query_builds_request(query_request):
    assert query_request.question == "What does main.py do?"
    assert query_request.top_k == 3


@pytest.mark.asyncio
async def test_query_default_top_k():
    req = QueryRequest(question="Hello")
    assert req.top_k is None


@pytest.mark.asyncio
@patch("services.retrieval.retrieve", new_callable=AsyncMock)
@patch("services.generation.generate", new_callable=AsyncMock)
async def test_query_pipeline(mock_generate, mock_retrieve):
    mock_retrieve.return_value = [
        {"text": "def main(): ...", "source": "main.py", "similarity": 0.92}
    ]
    mock_generate.return_value = "main.py defines the entry point."

    chunks = await mock_retrieve("What does main.py do?", top_k=3)
    answer = await mock_generate("What does main.py do?", chunks)

    assert len(chunks) == 1
    assert "entry point" in answer
