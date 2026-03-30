from typing import Dict, List, Optional
from uuid import uuid4

try:
    import chromadb
    from chromadb.utils import embedding_functions
except Exception:
    chromadb = None
    embedding_functions = None


class RagVectorStore:
    def __init__(
        self,
        persist_dir: str = "data/chroma",
        collection_name: str = "knowledge_base",
        embedding_model: str = "all-MiniLM-L6-v2",
    ) -> None:
        if chromadb is None or embedding_functions is None:
            raise RuntimeError(
                "RAG dependencies are missing. Install requirements.txt to enable Chroma retrieval."
            )
        self.client = chromadb.PersistentClient(path=persist_dir)
        embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_fn,
        )

    def upsert_chunks(self, chunks: List[Dict[str, str]]) -> int:
        if not chunks:
            return 0

        ids = [str(uuid4()) for _ in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [
            {
                "topic": chunk.get("topic", "general"),
                "subtopic": chunk.get("subtopic", "general"),
                "source": chunk.get("source", "unknown"),
            }
            for chunk in chunks
        ]

        self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
        return len(ids)

    def search(self, query: str, topic: Optional[str] = None, n_results: int = 4) -> List[Dict[str, str]]:
        where = {"topic": topic} if topic else None
        result = self.collection.query(query_texts=[query], n_results=n_results, where=where)

        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        dists = result.get("distances", [[]])[0]

        output = []
        for idx, doc in enumerate(docs):
            meta = metas[idx] if idx < len(metas) else {}
            dist = dists[idx] if idx < len(dists) else None
            output.append(
                {
                    "text": doc,
                    "topic": (meta or {}).get("topic", "general"),
                    "subtopic": (meta or {}).get("subtopic", "general"),
                    "source": (meta or {}).get("source", "unknown"),
                    "distance": dist,
                }
            )
        return output
