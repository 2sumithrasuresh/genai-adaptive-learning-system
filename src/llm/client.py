def call_llm(prompt: str) -> str:
    return f"""
[GENAI OUTPUT]

Prompt sent to model:
---------------------
{prompt}

(Replace this stub with a real LLM API later)
"""
