from abstract import PrivilegedTransaction
from .session import AdminSession, StdSession, LoggedOutSession
from .bankerror import BankError

# Changeplan transaction class, used to change the plan of an account
class Changeplan(PrivilegedTransaction):
    #Constructor
    def __init__(self, session):
        super().__init__(session, 8)

    # Perform the transaction
    def perform(self):
        if isinstance(self.session, AdminSession):
            # Prompt user to enter account name
            holder = input("Please enter the account holder's name: \n")
            
            # Raises error if user enters nothing or only whitespace characters
            if holder.isspace() or holder == "":
                raise BankError("Must enter a valid username")

            # Gets list of accounts from the bank file that match the entered username
            holder_accounts = [account for account in self.session.accounts if account.account_holder.name==holder]

            if holder_accounts:
                # Prompts user to enter the account number
                account_number = input("Please enter the account number: \n")

                # Raises error if user enters nothing or only whitespace characters
                if account_number.isspace() or account_number == "":
                    raise BankError("Must enter a valid account number")

                # Gets the first (and only) account from holder_accounts that matches the given account number
                bank_account = next((account for account in holder_accounts if account.account_number == int(account_number)), None)

                if bank_account:
                    # Each account must either have a Student or Non-Student plan, based on its boolean is_student value
                    old_plan = "Student" if (bank_account.is_student) else "Non-Student"
                    # Plan is being changed, so new plan must be the opposite of whatever it was previously
                    new_plan = "Non-Student" if (bank_account.is_student) else "Student"
                    
                    bank_account.is_student = not bank_account.is_student
                    print(f"{bank_account.account_holder.name}'s plan for account {bank_account.account_number:05.0f} has been changed from [{old_plan}] to [{new_plan}].")
                    self.log(bank_account)
                else:
                    raise BankError("Account number does not match account name")
            else:
                raise BankError("Account name does not exist")

        # Error if user is standard or logged out
        elif isinstance(self.session, StdSession):
            raise BankError("Must be admin")
        elif isinstance(self.session, LoggedOutSession):
            raise BankError("Please login first")
    
    # Log the transaction
    def log(self, account, amount=0, tags="  "):
        if account.is_student:
            tags = "SP"
        else:
            tags = "NP"
        self.session.transaction_logs.append(f"0{self.transaction_num} {account.account_holder.name}\
{' ' * (20 - len(account.account_holder.name))} {account.account_number:05.0f} {amount:08.2f} {tags if tags else '  '}")

