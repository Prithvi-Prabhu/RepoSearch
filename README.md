# RepoSearch: RAG-based GitHub Repository Assistant

## Overview

RepoSearch is a full-stack AI application that allows users to ingest GitHub repositories and query them using natural language. It uses Retrieval-Augmented Generation (RAG) to provide context-aware answers and includes an evaluation pipeline to measure response quality.

---
<img width="1918" height="963" alt="image" src="https://github.com/user-attachments/assets/dbf4ed8e-9437-4fdf-99d1-6a3d2c7f84d6" />


## Features

* Ingest any public GitHub repository
* Ask questions about code, documentation, or structure
* Context-aware answers using RAG (LangChain + vector search)
* Evaluation metrics:

  * Faithfulness
  * Answer Relevancy
  * Context Precision & Recall
* Clean Streamlit dashboard with dark theme

---

## Tech Stack

* **Backend:** FastAPI
* **LLM:** Groq (LLaMA 3.1)
* **RAG Framework:** LangChain
* **Embeddings:** HuggingFace (MiniLM)
* **Vector Store:** FAISS
* **Frontend:** Streamlit

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/repo-search.git
cd repo-search
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add environment variables

Create a `.env` file:

```
GROQ_API_KEY=your_api_key
LANGCHAIN_API_KEY=your_api_key
HF_TOKEN=your_token (optional)
```

---

## Run the App

### Start backend

```bash
uvicorn app.main:app --reload
```

### Start frontend

```bash
streamlit run frontend/app.py
```

---

## Usage

1. Paste a GitHub repo URL in the sidebar and click **Ingest**
2. Ask questions in the Query section
3. View generated answers and sources
4. Run evaluation to see quality metrics

---

## Evaluation

The system includes a RAGAS-style evaluation pipeline that measures:

* **Faithfulness:** Is the answer grounded in retrieved context?
* **Answer Relevancy:** Does the answer address the question?
* **Context Precision/Recall:** Quality of retrieved documents

---

## Future Improvements

* Better chunking strategies for code
* Caching & faster retrieval
* Visualization for evaluation metrics
* Deployment (Streamlit Cloud / Render)

---


