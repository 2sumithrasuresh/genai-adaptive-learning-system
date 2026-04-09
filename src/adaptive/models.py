from pydantic import BaseModel

# POST /generate-question
# Input: { topic, difficulty }
# Output: { question, expected_answer }
class GenerateQuestionRequest(BaseModel):
    topic: str
    difficulty: int  # 1-5

class GenerateQuestionResponse(BaseModel):
    question: str
    expected_answer: str

# POST /evaluate-answer
# Input: { question, expected_answer, student_answer }
# Output: { correctness, score, mistake_type }
class EvaluateAnswerRequest(BaseModel):
    question: str
    expected_answer: str
    student_answer: str

class EvaluateAnswerResponse(BaseModel):
    correctness: str   # correct / partial / wrong
    score: float       # 0-1
    mistake_type: str  # conceptual / calculation / guess

# POST /update-student
# Input: { student_id, evaluation_result }
# Output: updated student state
class UpdateStudentRequest(BaseModel):
    student_id: str
    topic: str
    evaluation_result: EvaluateAnswerResponse

# POST /next-action
# Input: { student_state, evaluation_result }
# Output: { next_difficulty, explanation_type }
class NextActionRequest(BaseModel):
    student_id: str
    topic: str
    evaluation_result: EvaluateAnswerResponse

    # ADD THESE
    question: str
    student_answer: str
    expected_answer: str

class NextActionResponse(BaseModel):
    next_difficulty: int
    explanation_type: str  # simple / targeted / advanced
    explanation: str
