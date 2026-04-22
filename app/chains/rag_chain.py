from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from app.retrieval.retriever import retrieve
from app.core.config import GROQ_API_KEY

llm = ChatGroq(api_key=GROQ_API_KEY, model="llama-3.1-8b-instant")

from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("""
You are a code assistant. Analyze the repository and give a structured answer.

Context:
{context}

Question:
{question}

Answer in the following format:

### Summary
Give a 2-3 line overview of the repository.

### Key Concepts
- List main topics (e.g., arrays, loops, APIs)

### Important Functions / Methods
- Mention key functions and what they do

### Examples
- Show 1–2 short code examples if present

### Notes
- Any insights or observations

Keep it concise and clean. Use bullet points.
""")

def run(repo_id, query):
    docs = retrieve(repo_id, query)

    if not docs:
        return "No relevant info found", []

    context = "\n\n".join(d.page_content for d in docs)

    response = llm.invoke(prompt.format(context=context, question=query))
    return response.content, [d.metadata for d in docs]