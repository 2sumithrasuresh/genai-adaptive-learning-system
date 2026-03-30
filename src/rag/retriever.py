from typing import Dict, List

from src.content.topics import TOPICS
from src.rag.vector_store import RagVectorStore


def _fallback_chunks(topic: str) -> List[Dict[str, str]]:
    topic_record = TOPICS.get(topic) or TOPICS.get("Binary Search", {})
    answer = topic_record.get("answer", "No source context available.")
    return [
        {
            "text": answer,
            "topic": topic,
            "subtopic": "fallback",
            "source": "src/content/topics.py",
            "distance": None,
        }
    ]


def retrieve_context(topic: str, query: str, top_k: int = 4) -> List[Dict[str, str]]:
    """Retrieve top-K chunks from Chroma, with a safe fallback if index is empty/unavailable."""
    try:
        store = RagVectorStore()
        chunks = store.search(query=query, topic=topic, n_results=top_k)
        if chunks:
            return chunks
    except Exception:
        pass

    return _fallback_chunks(topic)
