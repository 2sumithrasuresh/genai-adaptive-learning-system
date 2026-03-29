from collections import defaultdict
from src.meta.logger import get_logs

def map_style(explanation_type):
    if explanation_type == "simple":
        return "definition"

    elif explanation_type == "targeted":
        return "step-by-step"

    elif explanation_type == "advanced":
        return "analogy"

    return "default"


def get_best_strategy(topic):
    logs = get_logs()

    scores = defaultdict(list)

    for log in logs:
        if log["topic"] == topic:
            scores[log["style"]].append(log["improvement_score"])

    avg_scores = {
        style: sum(vals)/len(vals)
        for style, vals in scores.items()
        if len(vals) > 0
    }

    if not avg_scores:
        return "step-by-step"

    return max(avg_scores, key=avg_scores.get)
