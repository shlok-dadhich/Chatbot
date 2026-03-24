"""
backend/threads.py
------------------
Manages the `thread_metadata` table in Postgres.
Provides helpers for saving, fetching, and deleting conversation threads.
"""

from __future__ import annotations

from backend.database import pool
from backend.rag import remove_thread_rag


# ── Schema init ───────────────────────────────────────────────────────────────

def init_thread_metadata_table() -> None:
    """Create the thread_metadata table if it does not already exist."""
    with pool.connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS thread_metadata (
                thread_id  TEXT PRIMARY KEY,
                user_id    TEXT,
                title      TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            ALTER TABLE thread_metadata
            ADD COLUMN IF NOT EXISTS user_id TEXT
        """)
        conn.execute("""
            UPDATE thread_metadata
            SET user_id = COALESCE(NULLIF(user_id, ''), 'u1')
            WHERE user_id IS NULL OR user_id = ''
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_thread_metadata_user_created
            ON thread_metadata (user_id, created_at DESC)
        """)
        conn.commit()


init_thread_metadata_table()


# ── CRUD ──────────────────────────────────────────────────────────────────────

def save_thread_title(thread_id: str, title: str, user_id: str) -> None:
    """Insert or update the title for a thread."""
    with pool.connection() as conn:
        conn.execute(
            """
            INSERT INTO thread_metadata (thread_id, user_id, title) VALUES (%s, %s, %s)
            ON CONFLICT (thread_id) DO UPDATE
            SET user_id = EXCLUDED.user_id,
                title = EXCLUDED.title
            """,
            (thread_id, user_id, title),
        )
        conn.commit()


def get_thread_metadata(user_id: str) -> dict:
    """Return {thread_id: {title, titled}} for one user, newest first."""
    with pool.connection() as conn:
        rows = conn.execute(
            """
            SELECT thread_id, title
            FROM thread_metadata
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,),
        ).fetchall()
    return {row[0]: {"title": row[1], "titled": True} for row in rows}


def delete_thread_conversation(thread_id: str, user_id: str) -> bool:
    """
    Permanently delete all checkpoints and metadata for a thread.
    Cleans: checkpoints, checkpoint_blobs, checkpoint_writes, thread_metadata,
            and in-process RAG state.
    """
    try:
        with pool.connection() as conn:
            owned = conn.execute(
                "SELECT 1 FROM thread_metadata WHERE thread_id = %s AND user_id = %s",
                (thread_id, user_id),
            ).fetchone()
            if not owned:
                return False

            for table in ("checkpoints", "checkpoint_blobs", "checkpoint_writes"):
                try:
                    conn.execute(f"DELETE FROM {table} WHERE thread_id = %s", (thread_id,))
                except Exception:
                    pass  # Table may not exist in all LangGraph versions
            conn.execute(
                "DELETE FROM thread_metadata WHERE thread_id = %s AND user_id = %s",
                (thread_id, user_id),
            )
            conn.commit()

        remove_thread_rag(thread_id)
        return True
    except Exception:
        return False
