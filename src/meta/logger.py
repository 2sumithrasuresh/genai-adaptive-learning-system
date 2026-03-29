explanation_logs = [
    {
        "topic": "deadlock",
        "style": "analogy",
        "improvement_score": 1
    },
    {
        "topic": "deadlock",
        "style": "definition",
        "improvement_score": 0.2
    }
]

def log_explanation(data):
    explanation_logs.append(data)

def get_logs():
    return explanation_logs
