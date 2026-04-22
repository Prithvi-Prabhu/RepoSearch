import ast
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    docs = []

    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                lines = code.splitlines()[node.lineno-1:node.end_lineno]
                docs.append(Document(
                    page_content="\n".join(lines),
                    metadata={"file": path, "type": "function"}
                ))
    except:
        pass

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs.extend(splitter.create_documents([code]))

    return docs