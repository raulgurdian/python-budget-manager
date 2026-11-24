# Interactive Personal Budget Manager — Release 1

A small, dependency-free Python CLI that records income and expenses, reports balances by currency, and imports/exports CSV. Built for **Session 10, Practice 1: Interactive Personal Budget Manager**.

## Requirements and setup

- Python **3.10+**; no third-party packages.
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

The tests cover normal add/report behavior, negative and zero amounts, duplicate IDs, missing fields, invalid dates, unsupported values, non-finite numbers, separate currencies, CSV round-trip, invalid import with row numbers, and a missing file.

## Data contract and input rules

Each transaction has exactly six fields: `id`, `date`, `kind`, `category`, `amount`, `currency`.

- `id`: unique, `T` followed by at least 3 digits (e.g., `T001`).
- `date`: actual calendar date formatted exactly `YYYY-MM-DD`.
- `kind`: `expense` or `income`.
- `category`: one of `entertainment`, `food`, `housing`, `other`, `salary`, `transport`.
- `amount`: positive, finite number converted to `float`.
- `currency`: `EUR` or `USD` (documented project restriction).
- Transactions with missing or extra fields are rejected; CSV imports are validated row by row and report the failing row.

## Modules

- `models.py`: record shape and field order.
- `validation.py`: consistent boundary validation.
- `services.py`: add, filter, and summarize records without I/O.
- `storage.py`: CSV save/load and import validation.
- `cli.py`: prompts, output and user-facing errors.

## Known limitations / Release 2 ideas

- The CLI saves/loads a default `transactions.csv` in the working directory; unsaved changes are lost upon exit.
- CSV save overwrites the destination file; always load before replacing stored data.
- Only EUR and USD are accepted; totals are separated by currency, with no exchange rate conversion.
- Monetary totals use floating-point arithmetic, sufficient for this introductory exercise but not ideal for financial accounting; a future release should use `Decimal`.
- No undo, editing, budget limits, authentication, or multi-user support (outside Release 1).
- A failed file write may leave a partially written destination; atomic saving could be added in Release 2.

## Submission evidence

See `DESIGN.md` for architecture rationale, `AI_DISCLOSURE.md` for assistance disclosure, `data/sample_transactions.csv` for valid sample records, and `data/invalid_transactions.csv` for a deliberate failing example.
