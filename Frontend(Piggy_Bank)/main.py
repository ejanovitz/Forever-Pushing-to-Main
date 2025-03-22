#!/bin/python3

# This is the bank application made for the Big Bank. 
# The application is made to be used by the bank's customers, as well as the bank's employees as admin.
# There is an input file that the app uses, which is a text file containing the current accounts of the bank.
# Meanwhile, the output is a text file that has transactions made by the customers.
# To get started, all of the code is in the src file. This main file is used to run the application.

# By: The Piggy Bank
# Date: 2/18/25
# Version: 0.1

# Main function, used to run the application
from src.bankui import BankUI
def main():
    bank_ui = BankUI()
    try:
        bank_ui.run()
    except EOFError:
        pass

if __name__ == "__main__":
    main()
