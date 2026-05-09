from groq import Groq
from app.retrieval.retriever import retrieve
from app.core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

PROMPT_TEMPLATE = """You are a code assistant. Analyze the repository and give a structured answer.

Context:
{context}

Question:
{question}

Answer in the following format:

### Summary
- Give a 2-3 line overview of the repository.

### Key Concepts
- List main topics (e.g., arrays, loops, APIs)

### Important Functions / Methods
- Mention key functions and what they do

### Examples
- Show 1–2 short code examples if present

### Notes
- Any insights or observations

Keep it concise and clean. Use bullet points."""


def run(repo_id: str, query: str) -> tuple[str, list[dict]]:
    docs = retrieve(repo_id, query)

    if not docs:
        return "No relevant info found", []

    context = "\n\n".join(d["page_content"] for d in docs)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": PROMPT_TEMPLATE.format(context=context, question=query),
            }
        ],
        max_tokens=1000,
    )

    answer = response.choices[0].message.content
    sources = [d["metadata"] for d in docs]
    return answer, sources