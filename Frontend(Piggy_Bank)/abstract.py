from abc import ABC, abstractmethod
from src.account import BankAccount, AccountHolder
from src.bankerror import BankError

DEFAULT_HOLDER_MESSAGE = 'Enter account holder'
DEFAULT_NUMBER_MESSAGE = 'Enter account number'

# Session abstract class to store the session information
class Session(ABC):
    #Constructor
    def __init__(self, bank_ui):
        self.bank_ui = bank_ui
        self.transaction_logs: list[str] = []

    # Abstract method, will be implemented in the child classes
    @abstractmethod
    def input_local_account(self, holder_message = '', number_message = '') -> BankAccount:
        pass
    
    # Used to input the global account
    def input_global_account(self, holder_message = DEFAULT_HOLDER_MESSAGE, number_message = DEFAULT_NUMBER_MESSAGE) -> BankAccount:
        holder = self.input_account_holder(holder_message)
        number = input(f'{number_message}: \n')
        account = holder.get_account(number)
        if account.disabled:
            raise BankError('Account is disabled')
        return account

    # Used to input the account holder
    def input_account_holder(self, message = DEFAULT_HOLDER_MESSAGE) -> AccountHolder:
        name = input(f'{message}: \n')
        return self.bank_ui.get_account_holder(name)

    # Will be implemented in the child classes
    def input_positive_money(self, max_value, message = 'Please type in the amount you want to use for this transaction') -> float:
        amount = input(f'{message}: \n').strip()

        try:
            # Convert the input to a float
            value = float(amount)

            # Check if the value is positive and within the allowed range
            if value <= 0:
                raise BankError('Invalid amount entered')
            if value > max_value:
                raise BankError(f'Invalid amount entered')

            # Round to two decimal places
            fixed_value = round(value, 2)

            # Check if the original value matches the rounded value
            if abs(value - fixed_value) > 0.0001:  # Allow for minor floating-point inaccuracies
                raise BankError('Invalid amount entered')

            return fixed_value

        except ValueError:
            raise BankError('Invalid amount entered')
        except BankError as e:
            print(f"Error: {e}")
    
    # Will be implemented in the child classes
    @abstractmethod
    def can_perform_transaction(self, transaction) -> bool:
        pass

# Abstract class for transactions
class Transaction(ABC):
    #Constructor
    def __init__ (self, session: Session, transaction_num: int):
        self.session: Session = session
        self.transaction_num: int = transaction_num

    # Will be implemented in the child classes
    @abstractmethod
    def perform(self):
        pass
    
    # Log the transaction to the transaction logs
    def log_raw(self, transaction_num: int, account_holder: str, account_number: int, amount: float, tags: str):
        self.session.transaction_logs.append(f"0{transaction_num} {account_holder:20} {account_number:05} {amount:08.2f} {tags:2}")

    # Helper method to log the transaction
    def log(self, amount: float, account, tags):
        account_holder = '' if account == None else account.account_holder.name
        account_number = 0 if account == None else account.account_number

        self.log_raw(self.transaction_num, account_holder, account_number, amount, tags if tags != None else '')

# Standard transaction class, used for all
class StdTransaction(Transaction):
     #Constructor
     def __init__(self, session, transaction_num):
        super().__init__(session, transaction_num)

# Privileged transaction class, used for admin users
class PrivilegedTransaction(Transaction):
    #Constructor
    def __init__(self, session, transaction_num):
        super().__init__(session, transaction_num)


    
    
