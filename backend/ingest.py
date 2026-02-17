import os
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DATA_DIR,
    EMBEDDING_MODEL,
    SUPPORTED_EXTENSIONS,
    VECTOR_STORE_DIR,
)


def collect_files(data_dir: Path) -> list[Path]:
    """Recursively collect all supported files from the data directory."""
    files = []
    for root, _, filenames in os.walk(data_dir):
        for fname in filenames:
            fpath = Path(root) / fname
            if fpath.suffix in SUPPORTED_EXTENSIONS:
                files.append(fpath)
    return files


def load_documents(file_paths: list[Path]):
    """Load documents from the collected file paths."""
    docs = []
    for fpath in file_paths:
        try:
            loader = TextLoader(str(fpath), encoding="utf-8")
            loaded = loader.load()
            for doc in loaded:
                doc.metadata["source"] = str(fpath)
            docs.extend(loaded)
        except Exception as e:
            print(f"[WARN] Skipping {fpath}: {e}")
    return docs


def split_documents(documents):
    """Split documents into chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)


def build_vector_store(chunks):
    """Create a FAISS vector store from document chunks."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_store = FAISS.from_documents(chunks, embeddings)
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(VECTOR_STORE_DIR))
    print(f"[INFO] Vector store saved to {VECTOR_STORE_DIR}")
    return vector_store


def ingest():
    """Full ingestion pipeline: collect → load → split → embed → store."""
    print(f"[INFO] Scanning {DATA_DIR} for files...")
    files = collect_files(DATA_DIR)
    if not files:
        print("[WARN] No supported files found in data directory.")
        return

    print(f"[INFO] Found {len(files)} file(s). Loading...")
    documents = load_documents(files)

    print(f"[INFO] Loaded {len(documents)} document(s). Splitting into chunks...")
    chunks = split_documents(documents)

    print(f"[INFO] Created {len(chunks)} chunk(s). Building vector store...")
    build_vector_store(chunks)
    print("[INFO] Ingestion complete.")


if __name__ == "__main__":
    ingest()
