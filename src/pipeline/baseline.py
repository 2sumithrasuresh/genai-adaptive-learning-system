from llm.client import call_llm
from prompts.baseline import BASELINE_PROMPTS

def run_tier1(user_answer: str, correct_answer: str) -> str:
    """
    Tier-1 Baseline Logic:
    - Very simple correctness check
    - Select explanation style
    - Call GenAI
    """

    # Simple correctness heuristic (placeholder)
    is_correct = len(user_answer.strip()) > 20

    learner_state = "confident" if is_correct else "confused"
    prompt = BASELINE_PROMPTS[learner_state]

    final_prompt = f"""
Learner state: {learner_state}

Instruction:
{prompt}
"""

    return call_llm(final_prompt)
