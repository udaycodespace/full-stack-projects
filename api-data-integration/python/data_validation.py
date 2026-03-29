"""Runs SQL-based validation checks and surfaces results via pandas."""

import logging
from pathlib import Path
from typing import Iterable, List, Tuple

import pandas as pd

from python.db_connection import get_db_connection

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def parse_validation_queries(path: Path) -> Iterable[Tuple[str, str]]:
    buffer = []
    description = None
    queries: List[Tuple[str, str]] = []
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if line.startswith("--"):
            description = line.lstrip("- ")
            continue
        if not line:
            if buffer:
                queries.append((description or "validation query", "\n".join(buffer)))
                buffer = []
                description = None
            continue
        buffer.append(raw_line)
    if buffer:
        queries.append((description or "validation query", "\n".join(buffer)))
    return queries


def _validate():
    sql_path = Path(__file__).resolve().parents[1] / "sql" / "validation_queries.sql"
    queries = parse_validation_queries(sql_path)
    if not queries:
        logging.warning("No validation queries found at %s", sql_path)
        return

    with get_db_connection() as conn:
        for description, query in queries:
            df = pd.read_sql_query(query, conn)
            count = len(df.index)
            logging.info("%s -> %s rows", description, count)
            if count:
                print(f"{description} returned {count} row(s)")
                print(df)
            else:
                print(f"{description} returned no issues")


def main():
    _validate()


if __name__ == "__main__":
    main()
