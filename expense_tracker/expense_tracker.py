"""A beginner-friendly expense tracker. Requires only Python 3."""
import sqlite3
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

# Personal expenses stay on this computer, outside the GitHub repository.
DATA_FILE = Path.home() / ".toufik_expense_tracker" / "expenses.db"


def parse_amount(text):
    """Convert rupees to integer paise without floating-point rounding."""
    try:
        amount = Decimal(text.strip())
    except InvalidOperation:
        raise ValueError("Amount must be a number.") from None
    if not amount.is_finite() or not Decimal("0") < amount <= Decimal("1000000000"):
        raise ValueError("Enter an amount above 0 and at most 1,000,000,000.")
    paise = amount * 100
    if paise != paise.to_integral_value():
        raise ValueError("Use at most two decimal places.")
    return int(paise)


def money(paise):
    return f"INR {paise // 100:,}.{paise % 100:02d}"


def open_database(path=DATA_FILE):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            spent_on TEXT NOT NULL,
            category TEXT NOT NULL,
            amount_paise INTEGER NOT NULL CHECK (amount_paise > 0),
            note TEXT NOT NULL
        )
    """)
    connection.commit()
    return connection


def add_expense(connection, amount_text, category, note="", spent_on=None):
    amount = parse_amount(amount_text)
    category = category.strip().lower()
    note = note.strip()
    if not category or len(category) > 40:
        raise ValueError("Category must contain 1 to 40 characters.")
    if len(note) > 200:
        raise ValueError("Keep the note within 200 characters.")
    spent_on = date.fromisoformat(spent_on) if spent_on else date.today()
    with connection:
        connection.execute(
            "INSERT INTO expenses (spent_on, category, amount_paise, note) VALUES (?, ?, ?, ?)",
            (spent_on.isoformat(), category, amount, note),
        )


def list_expenses(connection):
    return connection.execute(
        "SELECT id, spent_on, category, amount_paise, note FROM expenses ORDER BY spent_on DESC, id DESC"
    ).fetchall()


def category_totals(connection):
    return connection.execute(
        "SELECT category, SUM(amount_paise) FROM expenses GROUP BY category ORDER BY category"
    ).fetchall()


def main():
    connection = open_database()
    try:
        print("PERSONAL EXPENSE TRACKER")
        print(f"Data saved locally: {DATA_FILE}")
        while True:
            print("\n1. Add expense\n2. View expenses\n3. Category summary\n4. Exit")
            choice = input("Choose 1-4: ").strip()
            try:
                if choice == "1":
                    amount = input("Amount in rupees (example: 120.50): ")
                    category = input("Category (food/travel/shopping/other): ")
                    note = input("Short note (optional): ")
                    spent_on = input("Date YYYY-MM-DD (Enter for today): ").strip()
                    add_expense(connection, amount, category, note, spent_on or None)
                    print("Expense saved!")
                elif choice == "2":
                    rows = list_expenses(connection)
                    if not rows:
                        print("No expenses yet. Choose 1 to add your first expense.")
                    for expense_id, spent_on, category, amount, note in rows:
                        print(f"#{expense_id} | {spent_on} | {category} | {money(amount)} | {note}")
                elif choice == "3":
                    totals = category_totals(connection)
                    if not totals:
                        print("No expenses yet.")
                    else:
                        for category, total in totals:
                            print(f"{category}: {money(total)}")
                        print(f"TOTAL: {money(sum(total for _, total in totals))}")
                elif choice == "4":
                    print("Goodbye!")
                    break
                else:
                    print("Please choose 1, 2, 3, or 4.")
            except ValueError as error:
                print(f"Invalid entry: {error}")
            except sqlite3.Error as error:
                print(f"Database operation failed: {error}")
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
    finally:
        connection.close()


if __name__ == "__main__":
    try:
        main()
    except (OSError, sqlite3.Error) as error:
        print(f"Could not open the local database: {error}")
