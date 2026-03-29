"""Validation helpers that surface dirty records before reporting."""
from typing import Dict

import pandas as pd

from .db_connection import get_connection

VALIDATION_QUERIES = {
    "negative_orders": "SELECT order_id, customer_id, amount, status FROM orders WHERE amount <= 0;",
    "failed_payments": "SELECT payment_id, order_id, amount, failure_code FROM payments WHERE success = FALSE;",
}


def run_validations() -> Dict[str, int]:
    """Execute validation SQL and return counts keyed by scenario."""
    counts: Dict[str, int] = {}
    with get_connection() as conn:
        for label, sql in VALIDATION_QUERIES.items():
            df = pd.read_sql(sql, conn)
            counts[label] = int(df.shape[0])
    return counts
