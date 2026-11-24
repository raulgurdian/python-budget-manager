"""CSV persistence with transactional import validation."""
from __future__ import annotations

import csv
from pathlib import Path
from .models import FIELDNAMES
from .validation import validate_transaction


def save_transactions(transactions: list[dict], filename: str | Path) -> None:
    """Write all records to CSV; a prior invalid record must not be written."""
    checked = []
    ids: set[str] = set()
    for index, record in enumerate(transactions, start=2):
        try:
            row = validate_transaction(record, ids)
        except ValueError as error:
            raise ValueError(f"Row {index}: {error}") from error
        ids.add(row["id"])
        checked.append(row)

    path = Path(filename)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(checked)


def load_transactions(filename: str | Path) -> list[dict]:
    """Validate every CSV row before returning any imported data."""
    transactions: list[dict] = []
    ids: set[str] = set()
    with Path(filename).open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise ValueError("Row 1: CSV file is empty; expected six column headers.")
        if len(reader.fieldnames) != len(set(reader.fieldnames)) or set(reader.fieldnames) != set(FIELDNAMES):
            raise ValueError(f"Row 1: CSV headers must be: {', '.join(FIELDNAMES)}.")
        for line_number, row in enumerate(reader, start=2):
            if None in row:
                raise ValueError(f"Row {line_number}: too many columns.")
            try:
                validated = validate_transaction(row, ids)
            except ValueError as error:
                raise ValueError(f"Row {line_number}: {error}") from error
            ids.add(validated["id"])
            transactions.append(validated)
    return transactions
