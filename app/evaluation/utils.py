import re

def extract_score(text: str) -> float:
    """
    Extracts a float score from LLM output safely.
    """
    if not text:
        return 0.0

    match = re.search(r"\d*\.?\d+", text)
    return float(match.group()) if match else 0.0