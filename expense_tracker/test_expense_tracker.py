"""Run with: python -m unittest discover -s expense_tracker -v"""
import tempfile
import unittest
from pathlib import Path
from expense_tracker import (
    add_expense, category_totals, list_expenses, money, open_database, parse_amount,
)


class ExpenseTrackerTests(unittest.TestCase):
    def test_amount_validation(self):
        self.assertEqual(parse_amount(" 120.50 "), 12050)
        self.assertEqual(parse_amount("0.01"), 1)
        self.assertEqual(money(123456), "INR 1,234.56")
        for value in ["", "abc", "0", "-5", "NaN", "Infinity", "1.001", "1000000001"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_amount(value)

    def test_persistence_and_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "expenses.db"
            connection = open_database(path)
            try:
                add_expense(connection, "0.10", " Food ", "Tea", "2026-10-24")
                add_expense(connection, "0.20", "food", "Snack", "2026-10-24")
                add_expense(connection, "25", "travel", "Bus", "2026-10-23")
                self.assertEqual(category_totals(connection), [("food", 30), ("travel", 2500)])
                for kwargs in [
                    {"category": " "},
                    {"category": "food", "spent_on": "2026-02-30"},
                    {"category": "food", "note": "x" * 201},
                ]:
                    with self.assertRaises(ValueError):
                        add_expense(connection, "10", **kwargs)
                self.assertEqual(len(list_expenses(connection)), 3)
            finally:
                connection.close()
            reopened = open_database(path)
            try:
                self.assertEqual(len(list_expenses(reopened)), 3)
                self.assertEqual(list_expenses(reopened)[0][4], "Snack")
            finally:
                reopened.close()

    def test_empty_database(self):
        with tempfile.TemporaryDirectory() as directory:
            connection = open_database(Path(directory) / "empty.db")
            try:
                self.assertEqual(list_expenses(connection), [])
                self.assertEqual(category_totals(connection), [])
            finally:
                connection.close()


if __name__ == "__main__":
    unittest.main()
