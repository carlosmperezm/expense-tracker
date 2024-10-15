from typing import List, Any
from argparse import ArgumentParser
from datetime import datetime
import csv

FILE_NAME: str = "expenses.csv"


class Expense:

    def __init__(self, description: str, amount: float) -> None:
        self.descripton = description
        self.amount = amount
        self.date = datetime.now()

    def __str__(self) -> str:
        return (
            f"Expense: {self.descripton} , amount: ${self.amount} , date: {self.date}"
        )


def read_csv(file_name: str = FILE_NAME) -> List:
    existing_data: List = []
    try:
        with open(file_name, mode="r", newline="") as file:
            reader = csv.reader(file)
            header = next(reader)
            data: List = [row for row in reader]

    except FileNotFoundError:
        print("File not found. Creating a new one.")

    return data


def write_csv(expense: Expense, file_name: str = FILE_NAME) -> bool:
    data: List = read_csv()

    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Description", "Amount", "Date"])

        if len(data) > 0:
            for row in data:
                writer.writerow(row)
        writer.writerow([expense.descripton, expense.amount, expense.date])

    last_row = read_csv()[-1]
    return (
        last_row[0] == expense.descripton
        and last_row[1] == str(expense.amount)
        and last_row[2] == str(expense.date)
    )


def add_expense(description: str, amount: float) -> None:
    expense = Expense(description, amount)
    print(write_csv(expense))


def update_expense(id: int) -> None: ...


def delete_expense(id: int) -> None: ...


def all_expenses() -> List: ...


def summary_expenses(month: int = None, year: int = None) -> List: ...


def main() -> None:
    parser: ArgumentParser = ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    parser_add: ArgumentParser = subparser.add_parser("add", help="Add new expense")
    parser_add.add_argument(
        "--description", required=True, help="Set a description for this expense"
    )
    parser_add.add_argument(
        "--amount", type=float, required=True, help="Set a amount for this expense"
    )

    parser_update: ArgumentParser = subparser.add_parser(
        "update", help="Update a extisting expense"
    )
    parser_update.add_argument(
        "-id", help="Provide an id in order to update the correct expense"
    )

    parser_delete: ArgumentParser = subparser.add_parser(
        "delete", help="Delete a extisting expense"
    )
    parser_delete.add_argument(
        "-id", help="Provide an id in order to delete the correct expense"
    )

    parser_list: ArgumentParser = subparser.add_parser(
        "list", help="List all the expenses"
    )

    parser_summary: ArgumentParser = subparser.add_parser(
        "summary", help="Show a summary of all the expenses"
    )
    parser_update.add_argument("-month", help="Provide a month to filter the summary")
    parser_update.add_argument("-year", help="Provide a year to filter the summary")

    args = parser.parse_args()

    if args.command == "add":
        print(f"Adding expense: {args.description} for ${args.amount}")
        add_expense(args.description, args.amount)

    elif args.command == "list":
        for row in read_csv():
            print(row)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
