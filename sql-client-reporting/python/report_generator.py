"""Coordinate reporting SQL execution and CSV exports."""
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from .data_validation import run_validations
from .db_connection import get_connection

REPORT_QUERIES = [
    (
        "monthly_revenue",
        """
        WITH revenue AS (
            SELECT DATE_TRUNC('month', o.order_date) AS month, SUM(o.amount) AS gross_revenue
            FROM orders o
            WHERE o.status = 'completed'
            GROUP BY 1
        )
        SELECT month, gross_revenue
        FROM revenue
        ORDER BY month;
        """,
    ),
    (
        "top_customers",
        """
        WITH customer_totals AS (
            SELECT c.customer_id, c.name, COUNT(o.order_id) AS order_count, SUM(o.amount) AS lifetime_revenue
            FROM customers c
            LEFT JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'completed'
            GROUP BY c.customer_id
        )
        SELECT customer_id, name, order_count, lifetime_revenue
        FROM customer_totals
        ORDER BY lifetime_revenue DESC NULLS LAST
        LIMIT 20;
        """,
    ),
]


def _execute_query(sql: str) -> pd.DataFrame:
    with get_connection() as conn:
        return pd.read_sql(sql, conn)


def _timestamped_filename(base_name: str, timestamp: str) -> Path:
    file_name = f"{base_name}_{timestamp}.csv"
    return Path(file_name)


def generate_reports(output_dir: Path | None = None) -> list[Path]:
    """Run reporting SQL, validations, and export CSVs."""
    output_dir = Path(output_dir or Path("reports"))
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    exported_files: list[Path] = []
    for name, sql in REPORT_QUERIES:
        df = _execute_query(sql)
        target = output_dir / _timestamped_filename(name, timestamp)
        df.to_csv(target, index=False)
        exported_files.append(target)

    validation_counts = run_validations()
    validation_df = pd.DataFrame(
        [
            {"validation": key, "invalid_records": value}
            for key, value in validation_counts.items()
        ]
    )
    validation_target = output_dir / _timestamped_filename("validation_summary", timestamp)
    validation_df.to_csv(validation_target, index=False)
    exported_files.append(validation_target)

    return exported_files


def main() -> None:
    """Entry point for command-line execution."""
    exported = generate_reports()
    for path in exported:
        print("Exported", path)


if __name__ == "__main__":
    main()
