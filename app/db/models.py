from contextlib import contextmanager
from app.db.db import get_conn


@contextmanager
def db_cursor():
    """
    Context manager that provides a cursor and always closes
    the connection, even on error. Prevents connection leaks.
    """
    conn = get_conn()
    try:
        cur = conn.cursor()
        yield conn, cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def repo_exists(repo_id: str) -> bool:
    with db_cursor() as (conn, cur):
        cur.execute("SELECT 1 FROM repos WHERE id = %s", (repo_id,))
        return cur.fetchone() is not None


def insert_repo(repo_id: str, url: str) -> None:
    with db_cursor() as (conn, cur):
        cur.execute(
            "INSERT INTO repos (id, url) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING",
            (repo_id, url),
        )