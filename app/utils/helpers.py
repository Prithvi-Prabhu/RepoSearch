import hashlib

def get_repo_id(repo_url: str):
    return hashlib.md5(repo_url.encode()).hexdigest()