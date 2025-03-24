import os
import re
from read import read_old_bank_accounts
from write import write_new_current_accounts
from logger import Logger

# Declare a class to handle file operations
class FileHandler:
    transactions = []  # Global transactions list
    accounts = []  # Global accounts list
    logger = Logger()

    def read_transactions(inpfile):
        """ Reads transactions from the given file and appends them to the transactions list. """
        if not os.path.exists(inpfile):
            FileHandler.logger.log_error("Read Error", "File not found", f"{inpfile}")
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
        return (
                account['account_number'].zfill(5) +
                account['name'].upper().ljust(20) +
                account['status'].ljust(2) +
                f"{account['balance']:08.2f}" +  # 8 chars for balance
                str(account['total_transactions']).zfill(4) +
                "0000"
        )

    def validate_account(line):
        if len(line) != 43:
            return False

        fields = [
            (line[0:5], r'\d{5}'),  # Account number
            (line[5:25], r'[A-Z ]{20}'),  # Name
            (line[25:27], r'(A |D |SP|NP|00)'),  # Status (2-char codes)
            (line[27:36], r'\d{7}\.\d{2}'),  # Balance
            (line[36:40], r'\d{4}'),  # Transaction count
            (line[40:44], r'\d{4}'),  # Unused
        ]

        for value, pattern in fields:
            if not re.fullmatch(pattern, value):
                return False

        return True
    def write_new_bank_account_file(accounts, newMasterbankAccountFile):
        formatted_accounts = []
        account_nums = set()

        for account in accounts:
            status = account['status'].strip()
            if status not in ['A', 'D']:
                # print(f"  Adjusted invalid status '{status}' to 'A' for account {account['account_number']}")
                status = 'A'

            # 🔧 Clamp balance
            balance = float(account['balance'])
            if balance > 99999.99:
                # print(f"  Balance capped at 99999.99 for account {account['account_number']}")
                balance = 99999.99

            # 👇 Cleaned account
            cleaned_account = {
                'account_number': account['account_number'].zfill(5),
                'name': account['name'].strip().upper()[:20],
                'status': status,
                'balance': balance,
                'total_transactions': account['total_transactions']
            }

            line = FileHandler.format_account(cleaned_account)

            if not FileHandler.validate_account(line):
                # Skip without logging error
                continue

            account_num = line[:5]
            if account_num in account_nums:
                FileHandler.logger.log_constraint_error("Constraint Error", f"Duplicate account number: {account_num}")
                continue

            account_nums.add(account_num)
            formatted_accounts.append(line)

        # Sort the accounts by account number only
        formatted_accounts.sort(key=lambda acc: int(acc[:5]))

        with open(newMasterbankAccountFile, 'w') as f:
            for account in formatted_accounts:
                f.write(account + '\n')

        print('New bank account file written successfully:', newMasterbankAccountFile)


    def write_current_accounts_file(accounts, file_path):
        current_accounts = []

        for account in accounts:
            try:
                # Fix status to only 'A' or 'D' for compatibility with write.py
                status = account['status'].strip()
                if status not in ['A', 'D']:
                    # print(f"Adjusted invalid status '{status}' to 'A' for account {account['account_number']}")
                    status = 'A'
                # Check for balances above 99999.99
                balance = float(account['balance'])
                if balance > 99999.99:
                    # print(f" Balance capped at 99999.99 for account {account['account_number']}")
                    balance = 99999.99

                current_accounts.append({
                    'account_number': account['account_number'].zfill(5),
                    'name': account['name'].strip().upper()[:20],
                    'status': status,
                    'balance': balance
                })
            except ValueError:
                FileHandler.logger.log_constraint_error("Constraint Error", f"Invalid balance: {account}")
                continue

        write_new_current_accounts(current_accounts, file_path)
        print('New current account file written successfully:', file_path)