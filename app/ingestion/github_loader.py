import os
from git import Repo

def clone_repo(repo_url, repo_id):
    path = f"/tmp/{repo_id}"

    if os.path.exists(path):
        return path

    Repo.clone_from(repo_url, path, depth=1)
    return path