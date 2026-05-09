import sqlite3
import os

DB_PATH = os.path.join("data", "repos.db")


def get_conn() -> sqlite3.Connection:
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Creates the repos table if it doesn't exist. Call once at startup."""
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS repos (
                id   TEXT PRIMARY KEY,
                url  TEXT NOT NULL
            )
            """
        )
        conn.commit()