import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

BASE_INDEX_PATH = "data/indexes"

MAX_FILE_SIZE = 200_000  # 200KB
MAX_QUERY_LENGTH = 500