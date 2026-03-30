import json
from pathlib import Path
from typing import Dict, List, Optional

from src.rag.chunker import chunk_document

try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None


TEXT_EXTENSIONS = {".txt", ".md"}


def _read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _read_pdf_file(path: Path) -> str:
    if PdfReader is None:
        raise RuntimeError("pypdf is required to ingest PDF files")
    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def _extract_topic_from_name(path: Path) -> str:
    stem = path.stem.replace("_", " ").replace("-", " ").strip()
    return stem.title() if stem else "General"


def ingest_folder(
    input_dir: str,
    topic_override: Optional[str] = None,
    min_words: int = 300,
    max_words: int = 500,
) -> List[Dict[str, str]]:
    """Read PDF/TXT/MD files from a folder and convert to structured chunks."""
    base = Path(input_dir)
    if not base.exists() or not base.is_dir():
        raise ValueError(f"Invalid input directory: {input_dir}")

    chunks: List[Dict[str, str]] = []
    files = [p for p in base.rglob("*") if p.is_file()]

    for file_path in files:
        ext = file_path.suffix.lower()
        if ext not in TEXT_EXTENSIONS and ext != ".pdf":
            continue

        if ext == ".pdf":
            text = _read_pdf_file(file_path)
        else:
            text = _read_text_file(file_path)

        if not text.strip():
            continue

        topic = topic_override or _extract_topic_from_name(file_path)
        doc_chunks = chunk_document(
            text=text,
            topic=topic,
            source=str(file_path),
            min_words=min_words,
            max_words=max_words,
        )
        chunks.extend(doc_chunks)

    return chunks


def write_chunks_json(chunks: List[Dict[str, str]], output_path: str) -> None:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(chunks, indent=2), encoding="utf-8")


def run_ingestion(input_dir: str, output_path: str, topic_override: Optional[str] = None) -> int:
    chunks = ingest_folder(input_dir=input_dir, topic_override=topic_override)
    write_chunks_json(chunks, output_path)
    return len(chunks)
