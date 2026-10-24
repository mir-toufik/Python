# Personal Expense Tracker

A small Python command-line project for recording expenses in Indian rupees.

## Features

- Add an amount, category, optional note, and date.
- View expenses with the newest dates first.
- See totals by category and an overall total.
- Keep data between sessions using SQLite.
- Reject invalid amounts, empty categories, and invalid dates.
- Store money as integer paise for exact totals.

## Run

Requires Python 3.8 or newer; no extra packages are needed.

Download or clone this repository, open a terminal in its root folder, and run:

```bash
python expense_tracker/expense_tracker.py
```

On Windows, use `py` if `python` is unavailable. On macOS/Linux, try `python3`.

Choose **1** to add an expense, **2** to view entries, **3** to see the summary, or **4** to exit. For the date, press Enter to use the computer's current date.

Example entry:

```text
Amount: 120.50
Category: food
Note: Lunch
Date: 2026-10-24
```

Summary after this entry:

```text
food: INR 120.50
TOTAL: INR 120.50
```

## Where is the data?

The program creates `~/.toufik_expense_tracker/expenses.db` in your home folder, outside the repository. Data stays on your computer; this project does not sync it to GitHub. The database is not encrypted. Copy that file to back it up while the program is closed.

## Tests

From the repository root:

```bash
python -m unittest discover -s expense_tracker -v
```

Tests cover invalid input, exact decimal totals, empty data, and persistence after reopening the database.

## Learn from this project

- Functions, loops, and conditions
- Input validation and exception handling
- Dates and paths
- Decimal arithmetic
- SQLite and parameterized SQL queries
- Automated tests

Practice idea: add a monthly summary after understanding the category summary. This starter version supports adding and viewing expenses; editing and deleting are future exercises.
