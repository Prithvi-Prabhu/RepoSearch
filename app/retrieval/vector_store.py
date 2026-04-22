import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.core.config import BASE_INDEX_PATH

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_index_path(repo_id):
    return os.path.join(BASE_INDEX_PATH, repo_id)

def create_index(docs, repo_id):
    db = FAISS.from_documents(docs, embedding)
    db.save_local(get_index_path(repo_id))

def load_index(repo_id):
    path = get_index_path(repo_id)
    if not os.path.exists(path):
        return None
    return FAISS.load_local(
    path,
    embedding,
    allow_dangerous_deserialization=True
)