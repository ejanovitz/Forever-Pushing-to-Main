import os
import re
from read import read_old_bank_accounts
from write import write_new_current_accounts

# Declare a class to handle file operations
class FileHandler:
    transactions = []  # Global transactions list
    accounts = []  # Global accounts list

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

    def format_account(account):
        sections = account.split('_')
        # Should be split up into 5 sections
        if len(sections) != 5:
            return None

        formatted_sections = [
            # zfill fills in the remaining spots with zeroes so "23" turns to "00023"
            # ljust fills in the remaining spots with spaces so "John" turns to "John              "
            sections[0].zfill(5),  # NNNNN: right justified, filled with zeroes
            sections[1].ljust(20),  # AAAAAAAAAAAAAAAAAAAA: left justified, filled with spaces
            sections[2].ljust(1),  # S: left justified, filled with spaces
            sections[3].zfill(8),  # PPPPPPPP: right justified, filled with zeroes
            sections[4].zfill(4)  # TTTT: right justified, filled with zeroes
        ]

        return '_'.join(formatted_sections)

    def validate_account(line):
        if len(line) != 42:
            return False

        fields = [
            (line[0:5], r'\d{5}'),  # NNNNN -> account number
            (line[5:25], r'[A-Z ]{20}'),  # AAAAAAAAAAAAAAAAAAAA -> name
            (line[25], r'[AD]'),  # S -> status: A(Active) or D(Disabled)
            (line[26:34], r'\d{5}\.00'),  # PPPPPPPP -> balance (ends in .00)
            (line[34:38], r'\d{4}'),  # TTTT -> transaction count
            (line[38:42], r'\d{4}')  # unused
        ]

        return all(re.fullmatch(pattern, value) for value, pattern in fields)

    def write_new_bank_account_file(accounts, newMasterbankAccountFile):
        formatted_accounts = []

        for account in accounts:
            formatted_account = FileHandler.format_account(account)
            if not formatted_account or not FileHandler.validate_account(formatted_account):
                print(f'ERROR: Invalid account format: {account}')
                # Skip invalid ones instead of returning early
                continue

            formatted_accounts.append(formatted_account)

        # Sort by bank account number (first 5 digits)
        def get_account_number(account_line):
            # No need to split by underscores
            # 0-5 is account numbers
            return int(account_line[:5])

        # Sort the accounts by account number only
        formatted_accounts.sort(key=get_account_number)

        with open(newMasterbankAccountFile, 'w') as f:
            for account in formatted_accounts:
                f.write(account + '\n')

        print('New bank account file written successfully:', newMasterbankAccountFile)


    def write_current_accounts_file(accounts, file_path):
        current_accounts = []

        for account in accounts:
            parts = account.split('_')
            if len(parts) != 5:
                print(f"Skipping invalid account (wrong format): {account}")
                continue
            try:
                current_accounts.append({
                    'account_number': parts[0].zfill(5),
                    'name': parts[1].strip().upper()[:20], # turns "        Ethan" to "ETHAN"
                    'status': parts[2].strip(),
                    'balance': float(parts[3])  # assumes it's like "00110.00"
                })
            except ValueError:
                print(f"Skipping invalid account (bad balance): {account}")
                continue

        write_new_current_accounts(current_accounts, file_path)
        print('New current account file written successfully:', file_path)