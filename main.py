# YouTube link: https://www.youtube.com/watch?v=Dn1EjhcQk64&t=359s

import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
import  matplotlib.pyplot as plt

# from matplotlib.pyplot import pyplotlib as plt

# df = pd.read_csv


# class to help us working with our csv file
class CSV: # singleton class
    CSV_FILE = "./source/finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False) # create the CSV file if it does not exist

    @classmethod
    def add_entry2(cls, date, amount, category, description):
        # Read the existing CSV file
        df = pd.read_csv(cls.CSV_FILE)

        # Create a new entry
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }

        # Append the new entry to the DataFrame
        df = df._append(new_entry, ignore_index=True)

        # Write the updated DataFrame back to the CSV file
        df.to_csv(cls.CSV_FILE, index=False)


    @classmethod
    def add_entry(cls, date, amount, category, description):

        # Create a new entry
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }

        with open(cls.CSV_FILE, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=cls.COLUMNS)
            # If the file is empty, write the header
            # if file.tell() == 0: # I guess no need since we initialize the CSV file (TBD maybe we can discard the initializer)
            #     writer.writeheader()
            writer.writerow(new_entry)
        print("Entry added successfully.")


    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)
        mask = (df["date"] >= start_date) & (df["date"] <= end_date) # like query/filter
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print('No transactions found in the given date range')
        else:
            print(f"transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)})) # otherwise the date printour is mirrored as in USA
            # print(filtered_df)

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")
        return filtered_df

def plot_tranactions(df):

    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    df.set_index('date', inplace=True)



    # income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0) # Day frequency
    income_df = df.query('category == "Income"') \
                  .resample("D") \
                  .sum() \
                  .reindex(df.index, fill_value=0)

    expense_df = df.query('category == "Expense"') \
                  .resample("D") \
                  .sum() \
                  .reindex(df.index, fill_value=0)    # Day frequency


    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")

    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title('Income and Expenses Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()


# CSV.initialize_csv()
# CSV.add_entry("2023-10-01", 100.00, "Food", "Lunch at restaurant")
# CSV.add_entry2("2025-10-01", 150.00, "Gas", "Filling up my car")


def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of transaction (dd-mm-yyyy) or leave blank for todays date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a given date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ", allow_default=True)
            df = CSV.get_transactions(start_date, end_date)

            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_tranactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")


if __name__ == '__main__':
    main()