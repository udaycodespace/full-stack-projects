"""Pipeline runner that persists API payloads into PostgreSQL."""

import logging
from typing import Iterable, Dict

from python.api_client import APIClient
from python.db_connection import get_db_connection

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def ensure_api_source(cursor, name: str, base_url: str) -> int:
    cursor.execute("SELECT id FROM api_sources WHERE name = %s", (name,))
    row = cursor.fetchone()
    if row:
        return row["id"]
    cursor.execute(
        "INSERT INTO api_sources (name, base_url) VALUES (%s, %s) RETURNING id",
        (name, base_url),
    )
    return cursor.fetchone()["id"]


def upsert_users(cursor, source_id: int, users: Iterable[Dict]) -> int:
    rows = [
        (
            user["user_id"],
            source_id,
            user["name"],
            user["username"],
            user["email"],
            user.get("city"),
            user.get("company_name"),
        )
        for user in users
    ]
    cursor.executemany(
        """
        INSERT INTO users (user_id, api_source_id, name, username, email, city, company_name)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (user_id) DO UPDATE
        SET name = EXCLUDED.name,
            username = EXCLUDED.username,
            email = EXCLUDED.email,
            city = EXCLUDED.city,
            company_name = EXCLUDED.company_name
        """,
        rows,
    )
    return len(rows)


def upsert_records(cursor, source_id: int, records: Iterable[Dict]) -> int:
    rows = [
        (
            record["user_id"],
            source_id,
            record["external_id"],
            record["title"],
            record["body"],
        )
        for record in records
    ]
    cursor.executemany(
        """
        INSERT INTO records (user_id, api_source_id, external_id, title, body)
        VALUES (%s,%s,%s,%s,%s)
        ON CONFLICT (external_id, api_source_id) DO UPDATE
        SET title = EXCLUDED.title,
            body = EXCLUDED.body
        """,
        rows,
    )
    return len(rows)


def ingest():
    client = APIClient()
    users = client.fetch_users()
    records = client.fetch_posts()

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            user_source_id = ensure_api_source(cursor, "jsonplaceholder_users", f"{client.BASE_URL}/users")
            records_source_id = ensure_api_source(cursor, "jsonplaceholder_posts", f"{client.BASE_URL}/posts")

            users_count = upsert_users(cursor, user_source_id, users)
            logging.info("Ingested %d users from %s", users_count, client.BASE_URL + "/users")

            records_count = upsert_records(cursor, records_source_id, records)
            logging.info("Ingested %d records from %s", records_count, client.BASE_URL + "/posts")


def main():
    ingest()


if __name__ == "__main__":
    main()
