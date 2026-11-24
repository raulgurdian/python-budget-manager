"""Transaction representation and the six-field data contract."""
from __future__ import annotations

FIELDNAMES = ("id", "date", "kind", "category", "amount", "currency")


def create_transaction(identifier: str, date: str, kind: str,
                       category: str, amount: float, currency: str) -> dict:
    """Build a transaction record; validation occurs at entry boundaries."""
    return {
        "id": identifier,
        "date": date,
        "kind": kind,
        "category": category,
        "amount": amount,
        "currency": currency,
    }
