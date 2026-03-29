from llm.client import call_llm
from prompts.baseline import BASELINE_PROMPTS

from src.meta.meta_engine import process_explanation
from src.meta.strategy import get_best_strategy


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

    explanation_type = best_style

    # --- 3. Generate explanation ---
    final_prompt = f"""
Learner state: {learner_state}

Instruction:
{prompt}
"""

    explanation = call_llm(final_prompt)

    # --- 4. Meta processing ---
    meta_result = process_explanation(
        explanation=explanation,
        context=correct_answer,
        topic=topic,
        explanation_type=explanation_type,
        prev_correctness=prev_result,
        current_correctness=current_result,
        student_answer=user_answer,
        correct_answer=correct_answer
    )

    print("Meta Result:", meta_result)

    return explanation
