"""
Simple Personal Expense Analyzer.

Reads expenses from a CSV file, categorizes them,
computes summary statistics, and writes a text report.
"""

CATEGORIES = {
    "food": ["mcdonald", "kfc", "grocer"],
    "transport": ["train", "uber", "bus"],
    "entertainment": ["netflix", "cinema"],
}


def categorize_transaction(description):
    desc = description.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in desc:
                return category

    return "other"


def read_expenses(filename):
    transactions = []

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # skip header
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        parts = line.split(",")
        if len(parts) != 3:
            continue  # bad line

        date_str = parts[0].strip()
        description = parts[1].strip()
        amount_str = parts[2].strip()

        try:
            amount = float(amount_str)
        except ValueError:
            # invalid amount, skip this line
            continue

        category = categorize_transaction(description)

        transaction = {
            "date": date_str,
            "description": description,
            "amount": amount,
            "category": category,
        }

        transactions.append(transaction)

    return transactions

def summarize_by_category(transactions):
    totals = {}

    for t in transactions:
        cat = t["category"]
        amt = t["amount"]

        if cat not in totals:
            totals[cat] = 0.0

        totals[cat] += amt

    return totals


def overall_summary(transactions):
    total = 0.0
    largest = None

    for t in transactions:
        amt = t["amount"]
        total += amt
        if largest is None or amt > largest["amount"]:
            largest = t

    return total, largest



def write_report(filename, transactions):
    category_totals = summarize_by_category(transactions)
    total_spent, largest = overall_summary(transactions)

    with open(filename, "w", encoding="utf-8") as f:
        f.write("Expense Report\n")
        f.write("==============\n\n")

        f.write(f"Total spent: ${total_spent:.2f}\n\n")

        f.write("By category:\n")
        for cat, amt in category_totals.items():
            f.write(f"  {cat}: ${amt:.2f}\n")

        f.write("\nLargest purchase:\n")
        f.write(
            f"  {largest['date']} - {largest['description']} (${largest['amount']:.2f})\n"
        )


def main():
    transactions = read_expenses("expenses.csv")
    print("Loaded", len(transactions), "transactions")

    # Debug view (optional, you can comment this out later)
    for t in transactions:
        print(t)

    category_totals = summarize_by_category(transactions)
    total_spent, largest = overall_summary(transactions)

    print("\n=== SUMMARY ===")
    print(f"Total spent: ${total_spent:.2f}")
    print("By category:")
    for cat, amt in category_totals.items():
        print(f"  {cat}: ${amt:.2f}")

    print("\nLargest purchase:")
    print(f"  {largest['date']} - {largest['description']} (${largest['amount']:.2f})")

    write_report("report.txt", transactions)
    print("\nReport written to report.txt")


if __name__ == "__main__":
    main()
