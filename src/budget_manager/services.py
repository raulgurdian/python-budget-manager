"""Pure business operations; no printing, prompting, or filesystem I/O."""
from __future__ import annotations

from .validation import validate_transaction


def add_transaction(transactions: list[dict], record: dict) -> dict:
    """Validate and append a transaction; leave list unchanged on failure."""
    existing_ids = {item["id"] for item in transactions}
    validated = validate_transaction(record, existing_ids)
    transactions.append(validated)
    return validated


def filter_transactions(transactions: list[dict], *, kind: str | None = None,
                        category: str | None = None, currency: str | None = None) -> list[dict]:
    """Return matching transactions without mutating the source list."""
    return [row for row in transactions
            if (kind is None or row["kind"] == kind)
            and (category is None or row["category"] == category)
            and (currency is None or row["currency"] == currency)]


def summarize(transactions: list[dict]) -> dict[str, dict[str, float]]:
    """Return totals per currency; never mix EUR and USD without an FX rate."""
    result: dict[str, dict[str, float]] = {}
    for row in transactions:
        currency = row["currency"]
        if currency not in result:
            result[currency] = {"income": 0.0, "expenses": 0.0, "balance": 0.0}
        if row["kind"] == "income":
            result[currency]["income"] += row["amount"]
        else:
            result[currency]["expenses"] += row["amount"]
        result[currency]["balance"] = result[currency]["income"] - result[currency]["expenses"]
    return result


def category_expenses(transactions: list[dict]) -> dict[str, dict[str, float]]:
    """Group expense totals by currency and category."""
    report: dict[str, dict[str, float]] = {}
    for row in filter_transactions(transactions, kind="expense"):
        categories = report.setdefault(row["currency"], {})
        categories[row["category"]] = categories.get(row["category"], 0.0) + row["amount"]
    return report
