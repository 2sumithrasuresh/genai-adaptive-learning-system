from src.meta.scorer import score_explanation
from src.meta.logger import log_explanation
from src.meta.evaluator import compute_improvement
from src.meta.strategy import map_style

def process_explanation(
    explanation,
    context,
    topic,
    explanation_type,
    prev_correctness,
    current_correctness,
    student_answer=None,
    correct_answer=None
):
    # 1. Score explanation
    scores = score_explanation(
        explanation,
        context,
        student_answer,
        correct_answer
    )

    # 2. Compute improvement
    improvement = compute_improvement(prev_correctness, current_correctness)

    # 3. Map style
    style = map_style(explanation_type)

    # 4. Log everything
    log_explanation({
        "topic": topic,
        "explanation": explanation,
        "style": style,
        "clarity_score": scores.get("clarity_score", 0),
        "relevance_score": scores.get("relevance_score", 0),
        "improvement_score": improvement
    })

    return {
        "scores": scores,
        "improvement": improvement,
        "style": style
    }
