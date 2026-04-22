import os
from app.core.config import MAX_FILE_SIZE

ALLOWED_EXT = [".py", ".js", ".ts", ".md"]

def get_files(path):
    files = []

    for root, _, filenames in os.walk(path):
        if ".git" in root or "node_modules" in root:
            continue

        for f in filenames:
            full = os.path.join(root, f)

            if not any(f.endswith(ext) for ext in ALLOWED_EXT):
                continue

            if os.path.getsize(full) > MAX_FILE_SIZE:
                continue

            files.append(full)

    return files