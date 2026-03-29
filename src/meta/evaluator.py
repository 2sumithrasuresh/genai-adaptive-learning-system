def compute_improvement(prev_correctness, current_correctness):
    if prev_correctness == "wrong" and current_correctness == "correct":
        return 1

    elif prev_correctness == "partial" and current_correctness == "correct":
        return 0.7

    else:
        return 0
