from typing import Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.rag.generator import generate_explanation_text
from src.rag.ingestion import ingest_folder
from src.rag.retriever import retrieve_context
from src.rag.vector_store import RagVectorStore

app = FastAPI(title="Adaptive Explanations RAG API")


class RetrieveContextRequest(BaseModel):
    topic: str
    query: str
    top_k: int = Field(default=4, ge=1, le=10)


class GenerateExplanationRequest(BaseModel):
    topic: str
    query: str
    difficulty: int = Field(default=2, ge=1, le=5)
    explanation_type: str = "targeted"
    top_k: int = Field(default=4, ge=1, le=10)


class IngestRequest(BaseModel):
    input_dir: str
    topic_override: Optional[str] = None


@app.post("/retrieve-context")
def retrieve_context_endpoint(payload: RetrieveContextRequest) -> Dict[str, List[str]]:
    chunks = retrieve_context(topic=payload.topic, query=payload.query, top_k=payload.top_k)
    return {"chunks": [c["text"] for c in chunks]}


@app.post("/generate-explanation")
def generate_explanation_endpoint(payload: GenerateExplanationRequest) -> Dict[str, object]:
    chunks = retrieve_context(topic=payload.topic, query=payload.query, top_k=payload.top_k)
    _, explanation = generate_explanation_text(
        query=payload.query,
        difficulty=payload.difficulty,
        explanation_type=payload.explanation_type,
        chunks=chunks,
    )
    return {
        "explanation": explanation,
        "chunks": [c["text"] for c in chunks],
    }


@app.post("/ingest-knowledge")
def ingest_knowledge_endpoint(payload: IngestRequest) -> Dict[str, int]:
    chunks = ingest_folder(input_dir=payload.input_dir, topic_override=payload.topic_override)
    store = RagVectorStore()
    inserted = store.upsert_chunks(chunks)
    return {"chunks_indexed": inserted}
