"""Safe PostgreSQL connection provider for the integration pipeline."""

import os
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor


def _env_or_raise(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(f"Missing required environment variable {key}")
    return value


@contextmanager
def get_db_connection():
    """Yield a committed connection that rolls back on failure."""
    connection = None
    try:
        connection = psycopg2.connect(
            host=_env_or_raise("DB_HOST"),
            port=_env_or_raise("DB_PORT"),
            dbname=_env_or_raise("DB_NAME"),
            user=_env_or_raise("DB_USER"),
            password=_env_or_raise("DB_PASSWORD"),
            cursor_factory=RealDictCursor,
        )
        yield connection
        connection.commit()
    except Exception:
        if connection:
            connection.rollback()
        raise
    finally:
        if connection:
            connection.close()
