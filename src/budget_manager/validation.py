"""Checks applied when transactions enter from the CLI or a CSV file."""
from __future__ import annotations

from datetime import date as calendar_date
import math
import re
from .models import FIELDNAMES

CATEGORIES = frozenset({"food", "transport", "housing", "entertainment", "salary", "other"})
CURRENCIES = frozenset({"EUR", "USD"})
KINDS = frozenset({"income", "expense"})


def validate_transaction(record: dict, existing_ids=()) -> dict:
    """Validate a six-field record; return a normalized numeric copy.

    Raise ValueError with an actionable description for invalid records.
    The current list's IDs should be passed as existing_ids when adding.
    """
    if not isinstance(record, dict):
        raise ValueError("Transaction must be a dictionary.")

    missing = set(FIELDNAMES) - set(record)
    extra = set(record) - set(FIELDNAMES)
    if missing:
        raise ValueError(f"Missing fields: {', '.join(sorted(missing))}.")
    if extra:
        raise ValueError(f"Unknown fields: {', '.join(sorted(extra))}.")

    identifier = record["id"]
    if not isinstance(identifier, str) or not re.fullmatch(r"T\d{3,}", identifier):
        raise ValueError("id must use the format T001 (T followed by at least three digits).")
    if identifier in existing_ids:
        raise ValueError(f"Duplicate transaction ID: {identifier}.")

    value = record["date"]
    if not isinstance(value, str):
        raise ValueError("date must be a string in YYYY-MM-DD format.")
    try:
        parsed = calendar_date.fromisoformat(value)
    except ValueError:
        raise ValueError("date must be a valid date in YYYY-MM-DD format.") from None
    if parsed.isoformat() != value:
        raise ValueError("date must use YYYY-MM-DD format.")

    kind = record["kind"]
    if not isinstance(kind, str) or kind not in KINDS:
        raise ValueError("kind must be income or expense.")
    category = record["category"]
    if not isinstance(category, str) or category not in CATEGORIES:
        raise ValueError(f"category must be one of: {', '.join(sorted(CATEGORIES))}.")

    raw_amount = record["amount"]
    if isinstance(raw_amount, bool) or not isinstance(raw_amount, (int, float, str)):
        raise ValueError("amount must be a positive number.")
    if isinstance(raw_amount, str) and not raw_amount.strip():
        raise ValueError("amount must be a positive number.")
    try:
        amount = float(raw_amount)
    except (ValueError, OverflowError):
        raise ValueError("amount must be a positive number.") from None
    if not math.isfinite(amount) or amount <= 0:
        raise ValueError("amount must be greater than zero and finite.")

    currency = record["currency"]
    if not isinstance(currency, str) or currency not in CURRENCIES:
        raise ValueError(f"currency must be one of: {', '.join(sorted(CURRENCIES))}.")

    validated = record.copy()
    validated["amount"] = amount
    return validated
