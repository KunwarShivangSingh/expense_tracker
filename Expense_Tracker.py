import json
import os
from datetime import datetime
from pathlib import Path


DATA_FILE = Path("expenses.json")

def load_expenses():
    """Load expenses from JSON file."""
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_expenses(expenses):
    """Save expenses to JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2, ensure_ascii=False)

def add_expense(expenses):
    """Add a new expense."""
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return expenses

    category = input("Category (e.g. Food, Transport, Bills): ").strip() or "Other"
    description = input("Description (optional): ").strip()

    expense = {
        "id": max((e.get("id", 0) for e in expenses), default=0) + 1,
        "amount": amount,
        "category": category,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"\nAdded: {amount:.2f} - {category}")

def view_expenses(expenses):
    """Display all expenses."""
    if not expenses:
        print("No expenses yet.")
        return

    print("\n" + "=" * 60)
    print(f"{'Date':<20} {'Category':<12} {'Amount':>10}  Description")
    print("=" * 60)
    for e in expenses:
        desc = (e.get("description") or "")[:25]
        print(f"{e['date']:<20} {e['category']:<12} {e['amount']:>10.2f}  {desc}")
    print("=" * 60)

def view_summary(expenses):
    """Show total and breakdown by category."""
    if not expenses:
        print("No expenses yet.")
        return

    total = sum(e["amount"] for e in expenses)
    by_category = {}
    for e in expenses:
        cat = e["category"]
        by_category[cat] = by_category.get(cat, 0) + e["amount"]

    print("\n--- Summary ---")
    print(f"Total spent: {total:.2f}")
    print("\nBy category:")
    for cat, amt in sorted(by_category.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {amt:.2f}")
    print()

def delete_expense(expenses):
    """Delete an expense by ID."""
    view_expenses(expenses)
    if not expenses:
        return
    try:
        eid = int(input("Enter expense ID to delete (or 0 to cancel): "))
    except ValueError:
        print("Invalid ID.")
        return
    if eid == 0:
        return
    original_len = len(expenses)
    expenses[:] = [e for e in expenses if e.get("id") != eid]
    if len(expenses) < original_len:
        save_expenses(expenses)
        print("Expense deleted.")
    else:
        print("ID not found.")

def main():
    expenses = load_expenses()
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. View summary by category")
        print("4. Delete expense")
        print("5. Exit")
        choice = input("Choice (1-5): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            view_summary(expenses)
        elif choice == "4":
            delete_expense(expenses)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1-5.")

if __name__ == "__main__":
    main()