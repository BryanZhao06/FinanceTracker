from expense import Expense
import calendar
import datetime
from colors import green, blue

def main():
    print(f"Running Finance Tracker App!")
    expense_file_path = "expenses.csv"
    budget = 2000
    #Get user input for expense
    expense = get_user_expense()
    
    #Write their expense to a file
    save_expense_to_file(expense, expense_file_path)
    
    #Read file and summarize expenses
    summarize_expenses(expense_file_path, budget)

def get_user_expense():
    expense_name = input("Enter name of expense: ")
    expense_amount = float(input("Enter the expense amount: $"))

    expense_categories = [
        "Food", 
        "Entertainment", 
        "Transportation", 
        "Savings", 
        "Miscellaneous"
    ]

    while True:
        print("Select an expense category: ")
        for index, category_name in enumerate(expense_categories):
            print(f" {index + 1}. {category_name}")
        
        value_range = f"[1 - {len(expense_categories)}]"

        user_input = input(f"Enter a category number {value_range}: ")
        try:
            selected_index = int(user_input) - 1
            
            if selected_index in range(len(expense_categories)):
                selected_category = expense_categories[selected_index]
                new_expense = Expense(name = expense_name, category = selected_category, amount = expense_amount)
                return new_expense
            else:
                print(f"Invalid number! Please enter a category number {value_range} \n")
        except ValueError:
            print(f"An error occurred! You entered '{user_input}' which is not a number. Please try again! \n")

def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"Saving User Expense: {expense} to ", end = "")
    print(blue(f"{expense_file_path}"))
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")

def summarize_expenses(expense_file_path, budget):
    expenses: list[Expense] = []    
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(
                name = expense_name, 
                amount = float(expense_amount), 
                category = expense_category
            )
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount
    
    print("📋 Expenses by Category: ")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")

    total_spent = sum([expense.amount for expense in expenses]) #For every expense in expenses, 
    print(f"💳 Total Spent: ${total_spent:.2f}")                    #create a new list where each item 
                                                                #in the list is equal to the expenses amount
    remaining_budget = budget - total_spent
    print(f"💰 Budget Remaining: ${remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(green(f"💵 Budget per Day: ${daily_budget:.2f}"))

if __name__ == "__main__":
    main()