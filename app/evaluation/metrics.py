from langchain_groq import ChatGroq
from app.core.config import GROQ_API_KEY
from app.evaluation.utils import extract_score

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant"  
)

# ---------------------------
# Faithfulness
# ---------------------------
def faithfulness_score(question, context, answer):
    prompt = f"""
You are evaluating factual consistency.

Question: {question}
Context: {context}
Answer: {answer}

Is the answer fully supported by the context?

Score from 0 to 1.
Only return a number.
"""
    res = llm.invoke(prompt)
    return extract_score(res.content)


# ---------------------------
# Answer Relevancy
# ---------------------------
def answer_relevancy(question, answer):
    prompt = f"""
Evaluate how well the answer addresses the question.

Question: {question}
Answer: {answer}

Score from 0 to 1.
Only return a number.
"""
    res = llm.invoke(prompt)
    return extract_score(res.content)


# ---------------------------
# Context Precision
# ---------------------------
def context_precision(question, context):
    prompt = f"""
Evaluate how relevant the retrieved context is.

Question: {question}
Context: {context}

Score from 0 to 1.
Only return a number.
"""
    res = llm.invoke(prompt)
    return extract_score(res.content)


# ---------------------------
# Context Recall
# ---------------------------
def context_recall(expected_answer, context):
    prompt = f"""
Does the context contain enough information to answer correctly?

Expected Answer: {expected_answer}
Context: {context}

Score from 0 to 1.
Only return a number.
"""
    res = llm.invoke(prompt)
    return extract_score(res.content)