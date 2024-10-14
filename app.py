from typing import List

from argparse import ArgumentParser


def add_expense(description: str, amount: float) -> None: ...


def update_expense(id: int) -> None: ...


def delete_expense(id: int) -> None: ...


def all_expenses() -> List: ...


def summary_expenses(month: int = None, year: int = None) -> List: ...


def main() -> None:
    parser: ArgumentParser = ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    parser_add: ArgumentParser = subparser.add_parser("add", help="Add new expense")
    parser_add.add_argument("-description", help="Set a description for this expense")
    parser_add.add_argument("-amount", help="Set a amount for this expense")

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
