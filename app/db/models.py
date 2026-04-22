from app.db.db import get_conn

def repo_exists(repo_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM repos WHERE id=%s", (repo_id,))
    exists = cur.fetchone()

    conn.close()
    return exists is not None


def insert_repo(repo_id, url):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("INSERT INTO repos (id, url) VALUES (%s, %s)", (repo_id, url))
    conn.commit()
    conn.close()