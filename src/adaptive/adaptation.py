# Adaptation Logic — exactly as per plan
#
# IF correctness == wrong:
#     difficulty -= 1 (min 1)
#     explanation_type = "simple"
#
# IF correctness == partial:
#     difficulty = same
#     explanation_type = "targeted"
#
# IF correctness == correct:
#     difficulty += 1 (max 5)
#     explanation_type = "advanced"
#
# mastery_score:
#     correct  → +0.1
#     partial  → +0.05
#     wrong    → -0.02
#     clamp between 0 and 1

def get_next_action(current_difficulty: int, correctness: str) -> dict:
    if correctness == "wrong":
        next_difficulty = max(1, current_difficulty - 1)
        explanation_type = "simple"
    elif correctness == "partial":
        next_difficulty = current_difficulty
        explanation_type = "targeted"
    else:  # correct
        next_difficulty = min(5, current_difficulty + 1)
        explanation_type = "advanced"

    return {
        "next_difficulty": next_difficulty,
        "explanation_type": explanation_type
    }


def update_mastery(current_score: float, correctness: str) -> float:
    delta = {"correct": 0.1, "partial": 0.05, "wrong": -0.02}
    new_score = current_score + delta.get(correctness, 0)
    return round(max(0.0, min(1.0, new_score)), 4)