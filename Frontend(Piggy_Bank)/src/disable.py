from abstract import PrivilegedTransaction
from .session import AdminSession, StdSession, LoggedOutSession
from .bankerror import BankError

# Disable transaction class, used to disable an account
class Disable(PrivilegedTransaction):
    # Constructor
    def __init__(self, session):
        super().__init__(session, 7)
    
    # Perform the transaction
    def perform(self):
        if isinstance(self.session, AdminSession):
            # Prompt user to enter account name
            holder = input("Please enter the account holder's name: \n")
            
            # Raises error if user enters nothing or only whitespace characters
            if holder.isspace() or holder == "":
                raise BankError("Must enter a valid username")

            # Gets list of accounts from the bank file that match the entered username
            holder_accounts = [account for account in self.session.accounts if account.account_holder.name == holder]

            if holder_accounts:
                # Prompts user to enter the account number
                account_number = input("Please enter the account number: \n")

                # Raises error if user enters nothing or only whitespace characters
                if account_number.isspace() or account_number == "":
                    raise BankError("Must enter a valid account number")

                # Gets the first (and only) account from holder_accounts that matches the given account number
                bank_account = next(
                    (account for account in holder_accounts if account.account_number == int(account_number)),
                    None
                )

                if bank_account:
                    # Cannot disable an already-disabled account
                    if bank_account.disabled:
                        raise BankError("Account is already disabled")
                    # If account isn't disabled, then disable it
                    else:
                        bank_account.disabled = True
                        print(f"{bank_account.account_holder.name}'s account {bank_account.account_number:05.0f} has been disabled.")

                        # Get list of bank account lines in account file
                        with open("./bank_account.txt", "r") as file:
                            accounts = file.readlines()
                        self.log(bank_account)
                else:
                    raise BankError("Account number does not match account name")
            else:
                raise BankError("Account name does not exist")

        # Error if user is standard or logged out
        elif isinstance(self.session, StdSession):
            raise BankError("Must be admin")
        elif isinstance(self.session, LoggedOutSession):
            raise BankError("ERROR: Please login first")

    def log(self, account, amount=0, tags=None):
        self.session.transaction_logs.append(f"0{self.transaction_num} {account.account_holder.name}\
{' ' * (20 - len(account.account_holder.name))} {account.account_number:05.0f} {amount:08.2f} {tags if tags else '  '}")
