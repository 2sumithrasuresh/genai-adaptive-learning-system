from prompts.baseline import BASELINE_PROMPTS

from src.meta.meta_engine import process_explanation
from src.meta.strategy import get_best_strategy
from src.rag.retriever import retrieve_context
from src.rag.generator import generate_explanation_text


def _style_to_meta_explanation_type(style: str) -> str:
    if style == "definition":
        return "simple"
    if style == "step-by-step":
        return "targeted"
    if style == "analogy":
        return "advanced"
    return "targeted"


def run_tier1(user_answer: str, correct_answer: str, topic: str = "general") -> str:
    """
    Tier-1 Baseline Logic:
    - Simple correctness check
    - Strategy selection
    - Meta evaluation
    """

    # --- 1. Simple correctness heuristic ---
    is_correct = len(user_answer.strip()) > 20

    prev_result = "wrong"  # mock (since no history yet)
    current_result = "correct" if is_correct else "wrong"

    learner_state = "confident" if is_correct else "confused"
    prompt = BASELINE_PROMPTS[learner_state]

    # --- 2. Strategy selection ---
    best_style = get_best_strategy(topic)
    print("Chosen Strategy:", best_style)

    explanation_type = _style_to_meta_explanation_type(best_style)
    difficulty = 4 if is_correct else 2

    # --- 3. Retrieve context (RAG) ---
    query = f"Topic: {topic}. Student answer: {user_answer}. Correct answer: {correct_answer}."
    chunks = retrieve_context(topic=topic, query=query, top_k=4)

    # --- 4. Generate explanation grounded in retrieved chunks ---
    pedagogical_prompt = f"""
Learner state: {learner_state}

Instruction:
{prompt}
"""
    _, explanation = generate_explanation_text(
        query=pedagogical_prompt,
        difficulty=difficulty,
        explanation_type=explanation_type,
        chunks=chunks,
    )

    # --- 5. Meta processing ---
    meta_result = process_explanation(
        explanation=explanation,
        context="\n\n".join([chunk.get("text", "") for chunk in chunks]),
        topic=topic,
        explanation_type=explanation_type,
        prev_correctness=prev_result,
        current_correctness=current_result,
        student_answer=user_answer,
        correct_answer=correct_answer
    )

    print("Meta Result:", meta_result)

    return explanation
