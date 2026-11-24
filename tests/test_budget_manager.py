"""Release 1 acceptance tests using Python's built-in unittest."""
import csv
import tempfile
import unittest
from pathlib import Path
from budget_manager.models import create_transaction, FIELDNAMES
from budget_manager.validation import validate_transaction
from budget_manager.services import add_transaction, filter_transactions, summarize, category_expenses
from budget_manager.storage import save_transactions, load_transactions


def sample(identifier="T001", kind="expense", amount=18.5, currency="EUR", category="food"):
    return create_transaction(identifier, "2026-09-04", kind, category, amount, currency)


class BudgetManagerTests(unittest.TestCase):
    def test_normal_add_and_report(self):
        rows = []
        add_transaction(rows, sample("T001", "income", 100, category="salary"))
        add_transaction(rows, sample("T002", "expense", 18.5))
        self.assertEqual(summarize(rows)["EUR"], {"income": 100.0, "expenses": 18.5, "balance": 81.5})
        self.assertEqual(category_expenses(rows)["EUR"]["food"], 18.5)
        self.assertEqual(len(filter_transactions(rows, kind="expense")), 1)

    def test_boundary_negative_and_zero_amount(self):
        for amount in (-1, 0):
            with self.subTest(amount=amount), self.assertRaisesRegex(ValueError, "greater than zero"):
                validate_transaction(sample(amount=amount))

    def test_boundary_duplicate_id_does_not_mutate_list(self):
        rows = []
        add_transaction(rows, sample())
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            add_transaction(rows, sample())
        self.assertEqual(len(rows), 1)

    def test_missing_fields_and_invalid_date(self):
        with self.assertRaisesRegex(ValueError, "Missing fields"):
            validate_transaction({"id": "T001"})
        invalid = sample()
        invalid["date"] = "2026-02-30"
        with self.assertRaisesRegex(ValueError, "date"):
            validate_transaction(invalid)

    def test_unknown_category_currency_and_kind(self):
        for field, value in (("category", "holidays"), ("currency", "GBP"), ("kind", "refund")):
            bad = sample()
            bad[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_transaction(bad)

    def test_nonfinite_and_non_numeric_amounts(self):
        for amount in ("nan", "inf", "oops", True):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                validate_transaction(sample(amount=amount))

    def test_separate_currencies(self):
        rows = [sample("T001", amount=5), sample("T002", "income", 8, "USD", "salary")]
        summary = summarize(rows)
        self.assertEqual(summary["EUR"]["balance"], -5)
        self.assertEqual(summary["USD"]["balance"], 8)

    def test_csv_round_trip_preserves_float(self):
        rows = [sample(), sample("T002", "income", 200, category="salary")]
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "data.csv"
            save_transactions(rows, path)
            loaded = load_transactions(path)
            self.assertEqual(loaded, rows)
            self.assertIsInstance(loaded[0]["amount"], float)

    def test_import_reports_row_number(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "bad.csv"
            with path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
                writer.writeheader()
                writer.writerow(sample())
                writer.writerow(sample("T002", amount=-4))
            with self.assertRaisesRegex(ValueError, "Row 3:.*amount"):
                load_transactions(path)

    def test_sample_data_files(self):
        data_dir = Path(__file__).resolve().parent.parent / "data"
        self.assertEqual(len(load_transactions(data_dir / "sample_transactions.csv")), 5)
        expected = {
            "invalid_transactions.csv": "Row 2:.*amount",
            "invalid_zero_amount.csv": "Row 3:.*amount",
            "invalid_date.csv": "Row 3:.*date",
            "invalid_category.csv": "Row 3:.*category",
            "invalid_currency.csv": "Row 3:.*currency",
            "invalid_duplicate_id.csv": "Row 3:.*Duplicate",
            "invalid_header.csv": "Row 1:.*headers",
        }
        for filename, message in expected.items():
            with self.subTest(file=filename), self.assertRaisesRegex(ValueError, message):
                load_transactions(data_dir / filename)

    def test_file_not_found(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(FileNotFoundError):
                load_transactions(Path(temp_dir) / "missing.csv")


if __name__ == "__main__":
    unittest.main()
