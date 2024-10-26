from typing import List, Any, Iterable
from argparse import ArgumentParser
from datetime import datetime
import csv
import os

FILE_NAME: str = "expenses.csv"


class Expense:

    def __init__(self, description: str, amount: float, category: str) -> None:
        self.descripton = description
        self.amount = amount
        self.date = datetime.now()
        self.category = category

    def __str__(self) -> str:
        return (
            f"Expense: {self.descripton} , amount: ${self.amount} , date: {self.date}"
        )


class User:
    budget: float = 0.0


def read_csv(file_name: str = FILE_NAME) -> List:
    existing_data: List = []
    data: List = []
    try:
        with open(file_name, mode="r", newline="") as file:
            reader = csv.reader(file)
            header = next(reader)
            data = [row for row in reader]

    except FileNotFoundError:
        print("File not found. Creating a new one.")

    return data


def validate_budget(budget: float, total_expenses) -> bool:
    if budget < total_expenses:
        print("!!🚨 ALERT 🚨!! Your are exceding your budget.")
        print(f"Budget:{budget} < total expenses:{total_expenses}")

        if input("Is that ok? (y/n)").lower() != "y":
            print("Aborting...")
            return False

    return True


def read_budget(file_path: str = "user.txt") -> float:
    try:
        with open("user.txt", "r") as user_file:
            return float(user_file.readline())
    except FileNotFoundError:
        return 0.0


def write_csv(expense: Expense | Any, file_name: str = FILE_NAME) -> bool:
    data: List = []
    data = read_csv()
    last_id: int = 0
    budget: float = read_budget("user.txt")
    total_expenses: float = summary_expenses()

    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "Description", "Amount", "Date", "Category"])

        if len(data) > 0:
            for row in data:
                last_id = int(row[0])
                writer.writerow(row)

        last_id += 1

        if isinstance(expense, Expense) and validate_budget(
            budget, total_expenses + expense.amount
        ):

            writer.writerow(
                [
                    last_id,
                    expense.descripton,
                    expense.amount,
                    expense.date,
                    expense.category,
                ]
            )
        elif isinstance(expense, Iterable) and validate_budget(
            budget, total_expenses + expense[2]
        ):
            writer.writerow(expense)

    last_row = read_csv()[-1]
    return last_row[0] == str(last_id)


def add_expense(description: str, amount: float, category: str) -> None:
    expense = Expense(description, amount, category)
    print(write_csv(expense))


def update_expense(id: int) -> None:

    updated: str = "Expense Not Found"

    data: List = read_csv()
    os.remove(FILE_NAME)

    for row in data:
        if row[0] == id:
            description = input("Description: ")
            amount = float(input("Amount: "))
            write_csv([row[0], description, amount, row[3], row[4]])
            updated = "Updated succefully"
        else:
            write_csv(row)
    print(updated)


def delete_expense(id: int) -> None:
    data: List = read_csv()

    del data[id - 1]

    os.remove(FILE_NAME)

    for row in data:
        write_csv(row)


def all_expenses() -> None:
    for row in read_csv():
        print(row)


def summary_expenses(month: int | None = None, category: str | None = None) -> float:
    total: float = 0

    for row in read_csv():
        date_object = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S.%f")

        if month and int(month) == date_object.month:
            total += float(row[2])
        elif category and category == row[4]:
            total += float(row[2])
        else:
            total += float(row[2])

    return total


def budget(new_budget: float) -> float:
    file_path: str = "user.txt"

    if new_budget is None:
        return read_budget(file_path)

    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass

    User.budget = new_budget

    with open(file_path, "w") as user_file:
        user_file.write(str(User.budget))

    return User.budget


def main() -> None:
    parser: ArgumentParser = ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    parser_add: ArgumentParser = subparser.add_parser("add", help="Add new expense")
    parser_add.add_argument(
        "-description", required=True, help="Set a description for this expense"
    )
    parser_add.add_argument(
        "-amount", type=float, required=True, help="Set a amount for this expense"
    )
    parser_add.add_argument(
        "-category", required=True, help="Set a category for this product"
    )

    parser_update: ArgumentParser = subparser.add_parser(
        "update", help="Update a extisting expense"
    )
    parser_update.add_argument(
        "-id",
        required=True,
        help="Provide an id in order to update the correct expense",
    )

    parser_delete: ArgumentParser = subparser.add_parser(
        "delete", help="Delete a extisting expense"
    )
    parser_delete.add_argument(
        "-id", type=int, help="Provide an id in order to delete the correct expense"
    )

    parser_list: ArgumentParser = subparser.add_parser(
        "list", help="List all the expenses"
    )

    parser_summary: ArgumentParser = subparser.add_parser(
        "summary", help="Show a summary of all the expenses"
    )
    parser_summary.add_argument("-month", help="Provide a month to filter the summary")
    parser_summary.add_argument(
        "-category", help="Provide a category to filter the summary"
    )
    parser_budget: ArgumentParser = subparser.add_parser("budget", help="Set a budget")
    parser_budget.add_argument(
        "-new", type=float, help="Show the current status of your budget"
    )

    args = parser.parse_args()

    if args.command == "add":
        print(f"Adding expense: {args.description} for ${args.amount}")
        add_expense(args.description, args.amount, args.category)

    elif args.command == "list":
        all_expenses()
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "update":
        update_expense(args.id)
    elif args.command == "summary":
        print(
            "Total expenses: ",
            summary_expenses(month=args.month, category=args.category),
        )
    elif args.command == "budget":
        print(budget(args.new))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
