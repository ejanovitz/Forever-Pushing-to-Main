import os
from read import read_old_bank_accounts
# Declare a class to handle file operations
class FileHandler:
    transactions = []  # Global transactions list
    accounts = []  # Global accounts list

    @staticmethod
    def read_transactions(inpfile):
        """ Reads transactions from the given file and appends them to the transactions list. """
        if not os.path.exists(inpfile):
            print(f"Error: {inpfile} not found.")
            return

        with open(inpfile, 'r') as file:
            content = file.readlines()
            FileHandler.transactions.extend(content)  # Append to class-level transactions list
            print("Transactions loaded:", FileHandler.transactions)

    def read_old_bank_account_file(oldMasterbankAccountFile):
        accounts = read_old_bank_accounts(oldMasterbankAccountFile)
        print("Old bank accounts loaded:", accounts)
        return accounts

