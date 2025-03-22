import random
from abstract import Session, PrivilegedTransaction
from .session import AdminSession, StdSession, LoggedOutSession
from .bankerror import BankError
from .account import AccountHolder, BankAccount

# Create transaction class, used to create an account
class Create(PrivilegedTransaction):
    # Constructor
    def __init__(self, session: Session):
        super().__init__(session, 5)

    # Perform the transaction
    def perform(self):

        # Checks if the number is already in use
        def account_number_is_unique(number: int) -> bool:
            for holder in self.session.bank_ui.account_holders:
                for account in holder.accounts:
                    if account.account_number == number:
                        return False
            return True

        # Checks if the user can perform the transaction
        if not isinstance(self.session, AdminSession):
            raise BankError('Must be admin')

        # Generates a unique account number
        def get_unique_account_number(start) -> int:
            number = start
            while not account_number_is_unique(number):
                number += 1
            return number

        

        # Setup
        name = input('What is the account holders name: \n')
        if not (1 <= len(name) <= 20):
            raise BankError('Account holder name must be between 1 and 20 characters long')

        if name == 'END_OF_FILE':
            raise BankError('Invalid account holder name')

        balance = input('What is the initial balance: \n')
        try:
            balance = float(balance)
        except ValueError:
            raise BankError('Invalid initial balance')

        if not (0 <= balance <= 99999.99):
            raise BankError('Initial balance must be between $0 and $99999.99')

        # Ensure the number isn't one already created this session.
        number = get_unique_account_number(self.session.created_account_number + 1)
        self.session.created_account_number = number

        print(f'''Account created
holder: {name}
account number: {number:05}
balance: ${balance:.2f}''')

        # Log the transaction
        self.log_raw(self.transaction_num, name, number, balance, '')
