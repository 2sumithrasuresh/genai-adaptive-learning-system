from src.llm.client import call_llm

def score_explanation(explanation, context):
    prompt = f"""
You are an expert educator.

Evaluate the explanation below.

Explanation:
{explanation}

Context:
{context}

Return JSON:
{{
  "clarity_score": 0-1,
  "relevance_score": 0-1
}}
"""

    response = call_llm(prompt)

    try:
        return json.loads(response)
    except:
        return {
            "clarity_score": 0,
            "relevance_score": 0
        }
