"""Connection helpers for PostgreSQL."""
from contextlib import contextmanager
import os

import psycopg2
from psycopg2.extras import DictCursor


def _get_db_config() -> dict:
    return {
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": int(os.environ.get("DB_PORT", "5432")),
        "dbname": os.environ.get("DB_NAME", "reporting"),
        "user": os.environ.get("DB_USER", "report_user"),
        "password": os.environ.get("DB_PASSWORD", ""),
        "connect_timeout": int(os.environ.get("DB_TIMEOUT", "10")),
    }


@contextmanager
def get_connection():
    """Yield a cursor-backed connection and ensure cleanup."""
    config = _get_db_config()
    conn = psycopg2.connect(**config)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@contextmanager
def get_cursor(cursor_factory=DictCursor):
    """Provide a cursor tied to the connection context."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=cursor_factory) as cursor:
            yield cursor
