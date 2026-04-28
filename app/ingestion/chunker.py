import ast
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_file(path: str) -> list[dict]:
    """
    Returns a list of dicts with 'page_content' and 'metadata' keys.
    First tries AST-based function extraction for .py files,
    then falls back to recursive character splitting for all files.
    """
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    docs = []

    # AST-based function-level chunks for Python files
    if path.endswith(".py"):
        try:
            tree = ast.parse(code)
            lines = code.splitlines()
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    chunk = "\n".join(lines[node.lineno - 1 : node.end_lineno])
                    docs.append({
                        "page_content": chunk,
                        "metadata": {"file": path, "type": "function"},
                    })
        except Exception:
            pass

    # Sliding-window character split for everything else (and as a complement)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    for chunk in splitter.split_text(code):
        docs.append({
            "page_content": chunk,
            "metadata": {"file": path, "type": "chunk"},
        })

    return docs