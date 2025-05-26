from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {
    "I": "Income",
    "E": "Expense"
}

def get_date2(prompt, allow_default=False):
    """ Prompts the user for a date input and returns it as a datetime.date object."""
    while True:
        date_str = input(prompt)

        # If the input is empty and default is allowed, return today's date
        if allow_default and not date_str.strip():
            return datetime.today().strftime("%d-%m-%Y")
        try:
            # Attempt to parse the date string (Try parsing the date in the format "DD-MM-YYYY")
            valid_date = datetime.strptime(date_str, "%d-%m-%Y")
            return valid_date.strftime("%d-%m-%Y")
        except ValueError:
            print("Invalid date format. Please enter the date in dd-mm-yyyy format.")


def get_date(prompt, allow_default=False):
    """ Prompts the user for a date input and returns it as a datetime.date object."""
    date_str = input(prompt)

    # If the input is empty and default is allowed, return today's date
    if allow_default and not date_str.strip():
        return datetime.today().strftime(date_format)
    try:

        # Attempt to parse the date string (Try parsing the date in the format "DD-MM-YYYY")

        valid_date = datetime.strptime(date_str, date_format) # strptime is for parsing and strftime is for formatting

        return valid_date.strftime(date_format)
    except (TypeError, ValueError):
        print("Invalid date format. Please enter the date in dd-mm-yyyy format.")
        return get_date(prompt, allow_default) # recursive function instead of the while True loop


def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()  # Recursive call to prompt again


def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense):").strip()
    if category in CATEGORIES:
        return CATEGORIES[category]

    print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")
    return get_category()  # Recursive call to prompt again


def get_description():
    return input("Enter the description (optional): ").strip() or "No description provided"


