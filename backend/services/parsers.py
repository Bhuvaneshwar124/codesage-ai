from pathlib import Path


def parse_file(file_path: Path) -> str:
    """Read a file and return its text content."""
    return file_path.read_text(encoding="utf-8", errors="replace")
