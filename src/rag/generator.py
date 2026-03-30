from typing import Dict, List, Tuple

from src.llm.client import call_llm
from src.rag.context_builder import build_explanation_prompt


def generate_explanation_text(
    query: str,
    difficulty: int,
    explanation_type: str,
    chunks: List[Dict[str, str]],
) -> Tuple[str, str]:
    """Return (prompt_used, generated_explanation)."""
    prompt = build_explanation_prompt(
        query=query,
        difficulty=difficulty,
        explanation_type=explanation_type,
        chunks=chunks,
    )
    explanation = call_llm(prompt)
    return prompt, explanation
