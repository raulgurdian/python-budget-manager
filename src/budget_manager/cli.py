"""Command-line interaction; delegates domain rules and files to other modules."""
from __future__ import annotations

from pathlib import Path
from .models import FIELDNAMES
from .services import add_transaction, summarize, category_expenses
from .storage import load_transactions, save_transactions

DEFAULT_FILE = Path("transactions.csv")


def prompt_transaction() -> dict:
    """Collect strings; the validation boundary converts amount to float."""
    return {field: input(f"{field.capitalize()}: ").strip() for field in FIELDNAMES}


def print_summary(transactions: list[dict]) -> None:
    summary = summarize(transactions)
    if not summary:
        print("No transactions to report.")
        return
    for currency, values in sorted(summary.items()):
        print(f"{currency}: income={values['income']:.2f}, "
              f"expenses={values['expenses']:.2f}, balance={values['balance']:.2f}")
    for currency, categories in sorted(category_expenses(transactions).items()):
        print(f"{currency} expenses by category:")
        for category, amount in sorted(categories.items()):
            print(f"  {category}: {amount:.2f}")


def main() -> None:
    transactions: list[dict] = []
    while True:
        print("\n1. Add transaction\n2. List transactions\n3. Report\n"
              "4. Save CSV\n5. Load CSV\n6. Exit")
        try:
            choice = input("Choose an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        try:
            if choice == "1":
                add_transaction(transactions, prompt_transaction())
                print("Transaction added.")
            elif choice == "2":
                if not transactions:
                    print("No transactions yet.")
                for record in transactions:
                    print(" | ".join(str(record[field]) for field in FIELDNAMES))
            elif choice == "3":
                print_summary(transactions)
            elif choice == "4":
                if not transactions and DEFAULT_FILE.exists():
                    answer = input(f"No transactions in memory. Overwrite {DEFAULT_FILE} "
                                   "with an empty list? (y/n): ").strip().lower()
                    if answer != "y":
                        print("Save cancelled; file left unchanged.")
                        continue
                save_transactions(transactions, DEFAULT_FILE)
                print(f"Saved {len(transactions)} transactions to {DEFAULT_FILE}.")
            elif choice == "5":
                loaded = load_transactions(DEFAULT_FILE)
                transactions = loaded  # Replace only after whole file passes validation.
                print(f"Loaded {len(transactions)} transactions from {DEFAULT_FILE}.")
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid option; choose 1-6.")
        except FileNotFoundError:
            print(f"Error: {DEFAULT_FILE} not found. Add transactions and save (option 4) first.")
        except (ValueError, OSError) as error:
            print(f"Error: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
