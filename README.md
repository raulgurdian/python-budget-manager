# Interactive Personal Budget Manager — Release 1

A small, dependency-free Python CLI that records income and expenses, reports balances by currency, and imports/exports CSV. Built for **Session 10, Practice 1: Interactive Personal Budget Manager**.

## Requirements and setup

- Python **3.9+**; no third-party packages. On macOS/Linux the command may be `python3` instead of `python`.
- Clone or download this repository; open a terminal in the repository root.
- Set the source path so Python can find the package:

```bash
# macOS / Linux
export PYTHONPATH=src
# Windows PowerShell
$env:PYTHONPATH = "src"
```

## Run

```bash
python -m budget_manager
```

Options: **1** Add transaction, **2** List, **3** Report, **4** Save CSV, **5** Load CSV, **6** Exit.

### Example

Choose **1** and enter these values when prompted:

```text
Id: T001
Date: 2026-09-04
Kind: expense
Category: food
Amount: 18.50
Currency: EUR
```

Choose **3** to see a EUR balance of `-18.50` (when this is the only transaction); choose **4** to save `transactions.csv`. Restart and select **5** to load it, then **2** to list it. To explore the included sample data, copy `data/sample_transactions.csv` to `transactions.csv` before selecting **5**.

## Test

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

On Windows PowerShell after setting `PYTHONPATH`, use `python -m unittest discover -s tests -v`.

The tests cover normal add/report behavior, negative and zero amounts, duplicate IDs, missing fields, invalid dates, unsupported values, non-finite numbers, separate currencies, CSV round-trip, invalid import with row numbers, every file in `data/` (valid and invalid), and a missing file.

## Data contract and input rules

Each transaction has exactly six fields: `id`, `date`, `kind`, `category`, `amount`, `currency`.

- `id`: unique, `T` followed by at least 3 digits (e.g., `T001`).
- `date`: actual calendar date formatted exactly `YYYY-MM-DD`.
- `kind`: `expense` or `income`.
- `category`: one of `entertainment`, `food`, `housing`, `other`, `salary`, `transport`.
- `amount`: positive, finite number converted to `float`.
- `currency`: `EUR` or `USD` (documented project restriction).
- Transactions with missing or extra fields are rejected; CSV imports are validated row by row and report the failing row.

## Acceptance criteria

Each rule below is checked by the tests or by a sample file in `data/`.

| Input | Expected result |
|---|---|
| `T001, 2026-09-04, expense, food, 18.50, EUR` | Accepted; report shows EUR balance `-18.50` |
| Amount `-10` | Rejected: `amount must be greater than zero and finite.` |
| Amount `0` | Rejected: `amount must be greater than zero and finite.` |
| Amount `oops`, `nan` or `inf` | Rejected: amount must be a positive, finite number |
| Date `2026-02-30` or `10/09/2026` | Rejected: `date must be a valid date in YYYY-MM-DD format.` |
| Category `holidays` | Rejected: `category must be one of: entertainment, food, housing, other, salary, transport.` |
| Kind `refund` or `Expense` | Rejected: `kind must be income or expense.` (no silent case correction) |
| Currency `GBP` | Rejected: `currency must be one of: EUR, USD.` |
| ID `T001` added twice | Rejected: `Duplicate transaction ID: T001.`; list stays unchanged |
| EUR and USD transactions | Reported separately; never added together |
| CSV with a bad row 3 | Whole file rejected with `Row 3: ...`; current data is not replaced |
| Save then load | Same transactions come back, amounts as numbers |

### Sample data

- `data/sample_transactions.csv`: five valid transactions in EUR and USD.
- Invalid files, one broken rule each (copy one to `transactions.csv` and choose **5** to see the error):

| File | Expected error |
|---|---|
| `invalid_transactions.csv` | `Row 2: amount must be greater than zero and finite.` |
| `invalid_zero_amount.csv` | `Row 3: amount must be greater than zero and finite.` |
| `invalid_date.csv` | `Row 3: date must be a valid date in YYYY-MM-DD format.` |
| `invalid_category.csv` | `Row 3: category must be one of: ...` |
| `invalid_currency.csv` | `Row 3: currency must be one of: EUR, USD.` |
| `invalid_duplicate_id.csv` | `Row 3: Duplicate transaction ID: T001.` |
| `invalid_header.csv` | `Row 1: CSV headers must be: id, date, kind, category, amount, currency.` |

## Modules

- `models.py`: record shape and field order.
- `validation.py`: consistent boundary validation.
- `services.py`: add, filter, and summarize records without I/O.
- `storage.py`: CSV save/load and import validation.
- `cli.py`: prompts, output and user-facing errors.

## Known limitations / Release 2 ideas

- The CLI saves/loads a default `transactions.csv` in the working directory; unsaved changes are lost upon exit.
- CSV save overwrites the destination file; always load before replacing stored data. Saving an empty list over an existing file asks for confirmation first.
- Only EUR and USD are accepted; totals are separated by currency, with no exchange rate conversion.
- Monetary totals use floating-point arithmetic, sufficient for this introductory exercise but not ideal for financial accounting; a future release should use `Decimal`.
- No undo, editing, budget limits, authentication, or multi-user support (outside Release 1).
- A failed file write may leave a partially written destination; atomic saving could be added in Release 2.

## Reflection (exit ticket)

**What did I verify?** I verified that a CSV with an invalid row is rejected with its exact row number: `test_import_reports_row_number` writes a file whose second transaction has amount `-4`, and the test confirms the error is `Row 3: amount must be greater than zero and finite.` I also confirmed that adding a duplicate ID raises an error and leaves the transaction list unchanged.

**Which boundary changed my design?** Mixing currencies. My first idea was a single balance, but adding EUR and USD together without an exchange rate gives a meaningless number, so the report keeps separate totals for each currency.

**What would I refactor next?** In Release 2 I would change amounts from `float` to `Decimal` in `validation.py` and `services.py`, because floating-point arithmetic can cause small rounding errors in money totals.

## Submission evidence

See `DESIGN.md` for architecture rationale, `AI_DISCLOSURE.md` for assistance disclosure, `data/sample_transactions.csv` for valid sample records, and the `data/invalid_*.csv` files for deliberate failing examples (one per validation rule).
