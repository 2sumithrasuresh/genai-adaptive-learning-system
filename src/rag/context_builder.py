from typing import Dict, List


def build_context_block(chunks: List[Dict[str, str]]) -> str:
    if not chunks:
        return "No context retrieved."

    parts = []
    for i, chunk in enumerate(chunks, start=1):
        subtopic = chunk.get("subtopic", "general")
        source = chunk.get("source", "unknown")
        text = chunk.get("text", "")
        parts.append(f"[{i}] Subtopic: {subtopic} | Source: {source}\n{text}")
    return "\n\n".join(parts)


def build_explanation_prompt(
    query: str,
    difficulty: int,
    explanation_type: str,
    chunks: List[Dict[str, str]],
) -> str:
    context = build_context_block(chunks)

    return f"""
You are an adaptive tutor.

Student query:
{query}

Difficulty level: {difficulty} (1 easiest, 5 hardest)
Explanation type: {explanation_type}

Use ONLY the context below for factual grounding.
If context is limited, clearly say what is uncertain.

Context:
{context}

Now generate a clear explanation tailored to the given difficulty and explanation type.
""".strip()
