import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Keeps track of asked questions per session (in memory)
asked_questions = []


# Question Prompt (from plan):
# "Generate a {difficulty} level question on {topic} with a concise expected answer."
def generate_question(topic: str, difficulty: int) -> dict:
    difficulty_label = {1: "very easy", 2: "easy", 3: "medium", 4: "hard", 5: "very hard"}
    level = difficulty_label.get(difficulty, "medium")

    # Build avoid list so LLM doesn't repeat questions
    avoid_section = ""
    if asked_questions:
        avoid_list = "\n".join(f"- {q}" for q in asked_questions[-10:])
        avoid_section = f"\nDo NOT ask any of these questions that were already asked:\n{avoid_list}\n"

    prompt = f"""Generate a {level} level question on {topic} with a concise expected answer.
{avoid_section}
Return ONLY a JSON object, no extra text, no markdown:
{{
  "question": "your question here",
  "expected_answer": "concise correct answer here"
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    result = json.loads(raw.strip())

    # Remember this question to avoid repeating it
    asked_questions.append(result["question"])

    return result


# Evaluation Prompt (from plan):
# "Compare the student answer with the expected answer. Return JSON with:
#  correctness (correct/partial/wrong), score (0-1), mistake_type (conceptual/calculation/guess)"
def evaluate_answer(question: str, expected_answer: str, student_answer: str) -> dict:
    prompt = f"""Compare the student answer with the expected answer. Return JSON with:
- correctness (correct/partial/wrong)
- score (0-1)
- mistake_type (conceptual/calculation/guess/none)

Question: {question}
Expected Answer: {expected_answer}
Student Answer: {student_answer}

Return ONLY a JSON object, no extra text, no markdown:
{{
  "correctness": "correct" or "partial" or "wrong",
  "score": 0.0 to 1.0,
  "mistake_type": "conceptual" or "calculation" or "guess" or "none"
}}

Rules:
- correct  = score 0.8-1.0, mistake_type = "none"
- partial  = score 0.4-0.79
- wrong    = score 0.0-0.39
- conceptual = student misunderstood the idea
- calculation = right idea, wrong numbers or steps
- guess = answer is unrelated or random"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())