import re
from fastapi import HTTPException

def validate_repo_url(url: str):
    pattern = r"^https://github\.com/[\w\-]+/[\w\-]+$"
    if not re.match(pattern, url):
        raise HTTPException(status_code=400, detail="Invalid GitHub URL")