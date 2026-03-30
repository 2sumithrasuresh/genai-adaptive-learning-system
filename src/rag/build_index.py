import argparse

from src.rag.ingestion import ingest_folder
from src.rag.vector_store import RagVectorStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Build RAG vector index from documents")
    parser.add_argument("--input-dir", required=True, help="Folder with .pdf/.txt/.md files")
    parser.add_argument("--topic", default=None, help="Optional topic override")
    args = parser.parse_args()

    chunks = ingest_folder(input_dir=args.input_dir, topic_override=args.topic)
    store = RagVectorStore()
    indexed = store.upsert_chunks(chunks)

    print(f"Indexed {indexed} chunks from {args.input_dir}")


if __name__ == "__main__":
    main()
