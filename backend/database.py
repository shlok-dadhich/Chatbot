"""
backend/database.py
-------------------
Sets up the shared PostgreSQL connection pool, LangGraph checkpointer (conversation
persistence) and LangGraph store (long-term memory).
"""

import atexit

from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore

from backend.config import DB_URI

# ── Shared connection pool ────────────────────────────────────────────────────

pool = ConnectionPool(
    conninfo=DB_URI,
    max_size=20,
    kwargs={"autocommit": True, "prepare_threshold": 0},
)


def _close_pool() -> None:
    try:
        pool.close()
    except Exception:
        # Avoid shutdown-time exceptions from bubbling during interpreter finalization.
        pass


atexit.register(_close_pool)

# ── Checkpointer — persists per-thread conversation history ──────────────────

checkpointer = PostgresSaver(pool)
checkpointer.setup()

# ── Store — persists cross-thread long-term memories ─────────────────────────

postgres_store = PostgresStore(pool)
postgres_store.setup()
