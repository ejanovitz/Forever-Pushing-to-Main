from abstract import Session, PrivilegedTransaction, DEFAULT_NUMBER_MESSAGE, DEFAULT_HOLDER_MESSAGE
from .account import BankAccount
from .bankerror import BankError

# Standard session class, used for standard users
class StdSession(Session):
     # Constructor
    def __init__(self, account_holder, bank_ui):
        super().__init__(bank_ui=bank_ui)  # Pass bank_ui to the parent class
        self.account_holder = account_holder
        # Used to enforce $500 session withdrawal limit
        self.amount_withdrawn = 0.0

    # Local account input, is only the first account for standard users
    def input_local_account(self, holder_message = DEFAULT_HOLDER_MESSAGE, number_message = DEFAULT_NUMBER_MESSAGE) -> BankAccount:
        number = input(f'{number_message}: \n')
        account = self.account_holder.get_account(number)
        if account.disabled:
            raise BankError('Account is disabled')
        return account
    
    # Can perform transaction, used to check if the user can perform the transaction
    def can_perform_transaction(self, transaction):
        if isinstance(transaction, PrivilegedTransaction):
            print('Sorry, but you cannot perform this transaction!')
            return False
        
        return True

# Admin session class, used for admin users
class AdminSession(Session):
    #Constructor
    def __init__(self, bank_ui):
        super().__init__(bank_ui=bank_ui)
        self.accounts = []
        # used to make sure accounts created this session have unique
        # account numbers from each other.
        self.created_account_number = 0
    
    # not needed?
    def input_local_account(self, holder_message = DEFAULT_HOLDER_MESSAGE, number_message = DEFAULT_NUMBER_MESSAGE):
        return self.input_global_account(holder_message, number_message)
    
    #will always return true
    def can_perform_transaction(self, transaction):
        return True;

# Logged out session class, used for when the user is not logged in
class LoggedOutSession(Session):
    pass
