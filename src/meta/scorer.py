import json
import re
from src.llm.client import call_llm

def score_explanation(explanation, context, student_answer=None, correct_answer=None):
    prompt = f"""
You are an expert educator.

Evaluate the explanation based on:

1. Clarity (is it easy to understand?)
2. Relevance (does it match the concept?)
3. Helpfulness (does it address the student's mistake?)

Student Answer:
{student_answer}

Correct Answer:
{correct_answer}

Explanation:
{explanation}

Return ONLY JSON:
{{
  "clarity_score": 0-1,
  "relevance_score": 0-1,
  "helpfulness_score": 0-1
}}
"""

    response = call_llm(prompt)

    try:
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass

    return {
        "clarity_score": 0,
        "relevance_score": 0,
        "helpfulness_score": 0
    }
