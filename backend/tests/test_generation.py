from services.generation import _build_prompt, _SYSTEM_PROMPTS


def test_build_prompt_document_qa():
    chunks = [{"source": "readme.md", "text": "Installation steps"}]
    prompt = _build_prompt("How do I install?", chunks, mode="document_qa")
    assert "Installation steps" in prompt
    assert "How do I install?" in prompt
    assert "document" in _SYSTEM_PROMPTS["document_qa"].lower()


def test_build_prompt_code_assistant():
    chunks = [{"source": "main.py", "text": "def main(): pass"}]
    prompt = _build_prompt("What does main do?", chunks, mode="code_assistant")
    assert "def main(): pass" in prompt
    assert "code" in _SYSTEM_PROMPTS["code_assistant"].lower()


def test_build_prompt_with_history():
    chunks = [{"source": "auth.py", "text": "class Auth: ..."}]
    history = [{"query": "What is Auth?", "response": "Auth is the auth class."}]
    prompt = _build_prompt("Tell me more.", chunks, mode="document_qa", history=history)
    assert "Conversation History" in prompt
    assert "What is Auth?" in prompt
    assert "Auth is the auth class." in prompt


def test_build_prompt_no_history():
    chunks = [{"source": "app.py", "text": "app = FastAPI()"}]
    prompt = _build_prompt("What is app?", chunks)
    assert "Conversation History" not in prompt


def test_default_mode_is_document_qa():
    chunks = [{"source": "x.py", "text": "x = 1"}]
    prompt = _build_prompt("q?", chunks)
    assert _SYSTEM_PROMPTS["document_qa"] in prompt
