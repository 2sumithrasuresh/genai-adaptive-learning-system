import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, get_connection
from models import (
    GenerateQuestionRequest, GenerateQuestionResponse,
    EvaluateAnswerRequest, EvaluateAnswerResponse,
    UpdateStudentRequest,
    NextActionRequest, NextActionResponse
)
from llm import generate_question, evaluate_answer
from adaptation import get_next_action, update_mastery

app = FastAPI(title="Adaptive Explanations Engine - Person 1")

# Fix CORS so React frontend can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup():
    init_db()


# ── POST /generate-question ───────────────────────────────────────
@app.post("/generate-question", response_model=GenerateQuestionResponse)
def generate_question_route(req: GenerateQuestionRequest):
    result = generate_question(req.topic, req.difficulty)
    return result


# ── POST /evaluate-answer ─────────────────────────────────────────
@app.post("/evaluate-answer", response_model=EvaluateAnswerResponse)
def evaluate_answer_route(req: EvaluateAnswerRequest):
    result = evaluate_answer(req.question, req.expected_answer, req.student_answer)

    session_id = str(uuid.uuid4())
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO attempt_logs
            (session_id, question, expected_answer, student_answer, correctness, score, mistake_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        session_id,
        req.question,
        req.expected_answer,
        req.student_answer,
        result["correctness"],
        result["score"],
        result["mistake_type"]
    ))
    conn.commit()
    cursor.close()
    conn.close()

    return EvaluateAnswerResponse(**result)


# ── POST /update-student ──────────────────────────────────────────
@app.post("/update-student")
def update_student(req: UpdateStudentRequest):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    eval_r = req.evaluation_result
    correctness = eval_r.correctness

    cursor.execute(
        "SELECT * FROM students WHERE id = %s AND topic = %s",
        (req.student_id, req.topic)
    )
    row = cursor.fetchone()

    if row is None:
        new_mastery = update_mastery(0.0, correctness)
        cursor.execute("""
            INSERT INTO students
                (id, topic, mastery_score, attempts, correct_count, wrong_count,
                 last_mistake_type, difficulty_level)
            VALUES (%s, %s, %s, 1, %s, %s, %s, 1)
        """, (
            req.student_id,
            req.topic,
            new_mastery,
            1 if correctness == "correct" else 0,
            1 if correctness == "wrong" else 0,
            eval_r.mistake_type
        ))
    else:
        new_mastery = update_mastery(row["mastery_score"], correctness)
        action = get_next_action(row["difficulty_level"], correctness)
        cursor.execute("""
            UPDATE students SET
                mastery_score = %s,
                attempts = attempts + 1,
                correct_count = correct_count + %s,
                wrong_count = wrong_count + %s,
                last_mistake_type = %s,
                difficulty_level = %s
            WHERE id = %s AND topic = %s
        """, (
            new_mastery,
            1 if correctness == "correct" else 0,
            1 if correctness == "wrong" else 0,
            eval_r.mistake_type,
            action["next_difficulty"],
            req.student_id,
            req.topic
        ))

    conn.commit()

    cursor.execute(
        "SELECT * FROM students WHERE id = %s AND topic = %s",
        (req.student_id, req.topic)
    )
    updated = cursor.fetchone()
    cursor.close()
    conn.close()
    return updated


# ── POST /next-action ─────────────────────────────────────────────
@app.post("/next-action", response_model=NextActionResponse)
def next_action(req: NextActionRequest):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT difficulty_level FROM students WHERE id = %s AND topic = %s",
        (req.student_id, req.topic)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")

    import httpx

    result = get_next_action(row["difficulty_level"], req.evaluation_result.correctness)

    # Build query for explanation engine
    query = f"""
    Topic: {req.topic}

    Question:
    {req.question}

    Correct Answer:
    {req.expected_answer}

    Student Answer:
    {req.student_answer}

    Evaluation:
    - correctness: {req.evaluation_result.correctness}
    - mistake_type: {req.evaluation_result.mistake_type}

    Instruction:
    Explain the correct concept clearly.
    Focus on fixing the student's mistake.
    Keep explanation aligned with the explanation_type.
    """

    try:
        exp_resp = httpx.post(
            "http://localhost:8001/generate-explanation",
            json={
                "topic": req.topic,
                "query": query,
                "difficulty": result["next_difficulty"],
                "explanation_type": result["explanation_type"]
            },
            timeout=30.0
        )
        explanation = exp_resp.json().get("explanation", "")
    except Exception as e:
        explanation = f"Explanation error: {str(e)}"

    return {
        "next_difficulty": result["next_difficulty"],
        "explanation_type": result["explanation_type"],
        "explanation": explanation
    }
