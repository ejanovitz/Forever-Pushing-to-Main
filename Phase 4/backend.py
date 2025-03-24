from file_handler import FileHandler
from transaction_processor import TransactionProcessor


# helper to convert dict to underscore account line
def convert_dict_to_account_line(acc):
    account_number = acc['account_number'].zfill(5)  # 5 characters, zero-padded
    name = acc['name'].upper().ljust(20)[:20]        # 20 characters, left-justified
    status = acc['status']                           # 1 character
    balance = f"{acc['balance']:08.2f}"              # 8 characters, zero-padded float
    txn_count = str(acc['total_transactions']).zfill(4)  # 4 characters
    unused = "0000"                                   # 4 characters unused

    # Final line must be 42 characters long
    return f"{account_number}{name}{status}{balance}{txn_count}{unused}"
def main():
    # Populate transactions array
    FileHandler.read_transactions("merged_transactions.txt")
    # Populate accounts array
    FileHandler.read_old_bank_account_file("master_file.txt")

    # iterate through transactions array and apply each transaction to the accounts array

    # Convert accounts list to a dictionary for easy lookup
    account_dict = {acc['account_number']: acc for acc in FileHandler.accounts}

    for transaction in FileHandler.transactions:
        transaction_type, name, account_number, amount, status = parse_transaction(transaction)

        if transaction_type == '00':  # Ignore end of transactions
            continue

        if account_number in account_dict:
            # Update existing account
            account = account_dict[account_number]
            account['balance'] += amount
            account['total_transactions'] += 1
            if status in ['SP', 'NP']:
                account['status'] = status  # Update status if it changed
        else:
            # Add new account
            new_account = {
                'account_number': account_number,
                'name': name,
                'status': status if status else 'A',  # Default to Active
                'balance': amount,
                'total_transactions': 1
            }
            account_dict[account_number] = new_account

    # Convert account dictionary back to list
    updated_accounts = list(account_dict.values())

    # Print updated accounts and total transaction cost
    print("Updated Accounts:")
    for acc in updated_accounts:
        print(acc)

    daily_transaction_cost = TransactionProcessor.daily_cost_per_plan("merged_transactions.txt")
    print("\nTotal Daily Transaction Cost:", daily_transaction_cost)

    formatted_accounts = [convert_dict_to_account_line(acc) for acc in updated_accounts]
    # Write new master accounts file
    FileHandler.write_new_bank_account_file(formatted_accounts, "new_master_file.txt")
    # Write new current accounts file
    FileHandler.write_current_accounts_file(formatted_accounts, "new_current_file.txt")

def parse_transaction(transaction):
    transaction_type = transaction[:2].strip()
    name = transaction[3:24].strip()
    account_number = transaction[25:30].strip()
    amount = float(transaction[31:37].strip()) / 100  # Convert cents to dollars
    status = transaction[41:].strip()
    return transaction_type, name, account_number, amount, status


main()
