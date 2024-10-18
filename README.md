# expense-tracker
This tiny project from roadmap.sh backend projects 

Sample solution for the [Expense Tracker](https://roadmap.sh/projects/expense-tracker) from [roadmap.sh](https://roadmap.sh)

This little app basically allows you to track your expenses:

1. Create a new Expense
2. Update an expense
3. Delete an expense
4. List all the expenses
5. Get a summary of your expenses
6. Get a summary by month as a filter.

## How to run
Clone the repository and run the following command:  
```
git clone https://github.com/carlosmperezm/expense-tracker.git
cd expense-tracker
```
Run poetry to install the app in orde to use the commands:
```
poetry install
```

There are a few commands you can use, here are some examples:

Add a new expense:
```
poetry run expense-tracker add -description "test" -amount 6
```
List all the expenses:
```
poetry run expense-tracker list
```
Update an expense
```
poetry run expense-tracker update -id 1
```
Summary of all the expenses:
```
poetry run expense-tracker summary
```
Summary of all the expenses made in october:
```
poetry run expense-tracker summary -month 10
```

### Notes:
The application will create a new expenses.csv file if not exists. In that way you have your expenses in csv format already :)


