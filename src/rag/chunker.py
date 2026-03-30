import re
from typing import Dict, List


def _looks_like_heading(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith("#"):
        return True
    if stripped.endswith(":") and len(stripped.split()) <= 12:
        return True
    if stripped.isupper() and 3 <= len(stripped.split()) <= 10:
        return True
    return False


def _split_sections(text: str) -> List[Dict[str, str]]:
    lines = text.splitlines()
    sections: List[Dict[str, str]] = []

    current_heading = "General"
    current_body: List[str] = []

    for line in lines:
        if _looks_like_heading(line):
            if current_body:
                sections.append({"subtopic": current_heading, "text": "\n".join(current_body).strip()})
                current_body = []
            current_heading = line.lstrip("#").strip(" :") or "General"
        else:
            current_body.append(line)

    if current_body:
        sections.append({"subtopic": current_heading, "text": "\n".join(current_body).strip()})

    return [sec for sec in sections if sec["text"]]


def _word_chunks(text: str, max_words: int) -> List[str]:
    words = re.findall(r"\S+", text)
    if not words:
        return []

    chunks = []
    step = max(1, max_words - 60)
    start = 0
    while start < len(words):
        end = min(start + max_words, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start += step
    return chunks


def chunk_document(
    text: str,
    topic: str,
    source: str,
    min_words: int = 300,
    max_words: int = 500,
) -> List[Dict[str, str]]:
    """Split document by headings and produce 300-500 word chunks with metadata."""
    if max_words < min_words:
        raise ValueError("max_words must be >= min_words")

    sections = _split_sections(text)
    all_chunks: List[Dict[str, str]] = []

    for sec in sections:
        subtopic = sec["subtopic"]
        section_text = sec["text"]

        words = section_text.split()
        if len(words) <= max_words:
            if len(words) < min_words and all_chunks:
                all_chunks[-1]["text"] += " " + section_text
            else:
                all_chunks.append(
                    {
                        "text": section_text,
                        "topic": topic,
                        "subtopic": subtopic,
                        "source": source,
                    }
                )
            continue

        for piece in _word_chunks(section_text, max_words=max_words):
            all_chunks.append(
                {
                    "text": piece,
                    "topic": topic,
                    "subtopic": subtopic,
                    "source": source,
                }
            )

    return all_chunks
