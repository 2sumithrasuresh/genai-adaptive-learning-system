"""
orchestrator.py — runSession loop (Person 1)

Exactly as per plan:
  runSession(student_id, topic):
    1. fetch student state
    2. call /generate-question
    3. receive student answer (frontend)
    4. call /evaluate-answer
    5. call /update-student
    6. call /next-action
    7. send explanation request (to Person 2 system)
    8. repeat
"""

import httpx
from typing import Callable

BASE_URL = "http://localhost:8000"


def run_session(
    student_id: str,
    topic: str,
    get_answer_fn: Callable[[str], str],
    max_questions: int = 10
):
    print(f"\nStarting session | student: {student_id} | topic: {topic}")

    # Step 1: fetch student state (check if exists, get difficulty)
    state_resp = httpx.get(f"{BASE_URL}/student/{student_id}/{topic}")
    if state_resp.status_code == 404:
        difficulty = 1
        print("New student — starting at difficulty 1")
    else:
        state = state_resp.json()
        difficulty = state["difficulty_level"]
        print(f"Returning student — difficulty: {difficulty}, mastery: {state['mastery_score']:.2f}")

    for i in range(max_questions):
        print(f"\n-- Question {i + 1} | difficulty {difficulty} --")

        # Step 2: call /generate-question
        q_resp = httpx.post(f"{BASE_URL}/generate-question", json={
            "topic": topic,
            "difficulty": difficulty
        })
        q_resp.raise_for_status()
        q_data = q_resp.json()
        question = q_data["question"]
        expected_answer = q_data["expected_answer"]
        print(f"Q: {question}")

        # Step 3: receive student answer (from frontend)
        student_answer = get_answer_fn(question)

        # Step 4: call /evaluate-answer
        eval_resp = httpx.post(f"{BASE_URL}/evaluate-answer", json={
            "question": question,
            "expected_answer": expected_answer,
            "student_answer": student_answer
        })
        eval_resp.raise_for_status()
        eval_result = eval_resp.json()
        print(f"Result: {eval_result['correctness']} | score: {eval_result['score']:.2f} | mistake: {eval_result['mistake_type']}")

        # Step 5: call /update-student
        update_resp = httpx.post(f"{BASE_URL}/update-student", json={
            "student_id": student_id,
            "topic": topic,
            "evaluation_result": eval_result
        })
        update_resp.raise_for_status()
        updated_state = update_resp.json()
        print(f"Mastery: {updated_state['mastery_score']:.2f}")

        # Step 6: call /next-action
        action_resp = httpx.post(f"{BASE_URL}/next-action", json={
            "student_id": student_id,
            "topic": topic,
            "evaluation_result": eval_result
        })
        action_resp.raise_for_status()
        action = action_resp.json()
        difficulty = action["next_difficulty"]
        print(f"Next difficulty: {difficulty} | explanation type: {action['explanation_type']}")

        # Step 7: send explanation request to Person 2's system
        explanation_request = {
            "student_id": student_id,
            "topic": topic,
            "question": question,
            "student_answer": student_answer,
            "expected_answer": expected_answer,
            "explanation_type": action["explanation_type"],
            "mastery_score": updated_state["mastery_score"]
        }
        # TODO: uncomment when Person 2 is ready
        # httpx.post("http://localhost:8001/generate-explanation", json=explanation_request)
        print(f"[Ready for Person 2]: {explanation_request}")

        # Step 8: repeat (loop continues)
        if updated_state["mastery_score"] >= 0.9:
            print(f"\nMastery reached! Session complete.")
            break

    print(f"\nSession done. Questions asked: {i + 1}")
    return updated_state


# Terminal test — run this directly to test without frontend
if __name__ == "__main__":
    run_session(
        student_id="student_001",
        topic="photosynthesis",
        get_answer_fn=lambda q: input(f"\n{q}\nYour answer: "),
        max_questions=5
    )