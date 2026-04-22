import json
from langchain_groq import ChatGroq
from app.core.config import GROQ_API_KEY

llm = ChatGroq(api_key=GROQ_API_KEY, model="llama-3.1-8b-instant")

# ─── Shared scoring helper ────────────────────────────────────────────────────

def _score(prompt: str) -> dict:
    """
    Asks the LLM to return a JSON object with `score` (0–1) and `reason`.
    Falls back to 0.0 on any parse error. Using JSON forces the model to
    be explicit about its reasoning, which also makes scores more reliable.
    """
    full_prompt = prompt + """

Respond ONLY with a valid JSON object. No extra text. Example:
{"score": 0.85, "reason": "The answer is mostly supported by the context but misses one detail."}
"""
    try:
        res = llm.invoke(full_prompt)
        data = json.loads(res.content)
        score = float(data.get("score", 0.0))
        reason = data.get("reason", "")
        return {"score": max(0.0, min(1.0, score)), "reason": reason}
    except Exception:
        return {"score": 0.0, "reason": "Parse error"}


# ─── Individual metrics ───────────────────────────────────────────────────────

def faithfulness_score(question: str, context: str, answer: str) -> dict:
    """
    Measures whether the answer is factually grounded in the context.
    High faithfulness = no hallucinations.
    """
    prompt = f"""You are an expert evaluator assessing factual grounding.

Question: {question}
Retrieved context: {context}
Generated answer: {answer}

Score how well the answer is supported ONLY by the provided context (not prior knowledge).
A score of 1.0 means every claim in the answer can be traced to the context.
A score of 0.0 means the answer introduces information not present in the context.
"""
    return _score(prompt)


def answer_relevancy(question: str, answer: str) -> dict:
    """
    Measures how directly the answer addresses the question.
    """
    prompt = f"""You are an expert evaluator assessing answer quality.

Question: {question}
Answer: {answer}

Score how directly and completely the answer addresses the question.
1.0 = fully addresses the question with no off-topic content.
0.0 = completely off-topic or empty.
"""
    return _score(prompt)


def context_precision(question: str, context: str) -> dict:
    """
    Measures the signal-to-noise ratio of the retrieved context.
    High precision = retrieved chunks are mostly relevant.
    """
    prompt = f"""You are an expert evaluator assessing retrieval quality.

Question: {question}
Retrieved context: {context}

Score what fraction of the retrieved context is actually relevant to answering the question.
1.0 = all retrieved content is useful for answering.
0.0 = retrieved content is entirely irrelevant.
"""
    return _score(prompt)


def context_recall(expected_answer: str, context: str) -> dict:
    """
    Measures whether the context contains enough info to produce the expected answer.
    High recall = retriever fetched the right documents.
    """
    prompt = f"""You are an expert evaluator assessing retrieval completeness.

Expected answer: {expected_answer}
Retrieved context: {context}

Score whether the retrieved context contains enough information to produce the expected answer.
1.0 = context has everything needed to derive the expected answer.
0.0 = context is missing all key information.
"""
    return _score(prompt)