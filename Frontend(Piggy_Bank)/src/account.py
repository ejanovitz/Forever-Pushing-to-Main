from .bankerror import BankError

# Bank Account Class, used for storing account information
class BankAccount:
    #Global Variables
    MAXIMUM_BALANCE = 99999.99
    ACCOUNT_NUMBER_DIGITS = 5

    #Constructor
    def __init__(self, account_holder, account_number: int, balance: float, disabled: bool, is_student: bool):
        self.account_holder: AccountHolder = account_holder
        self.account_number: int = account_number
        self.balance: float = balance
        self.usable: float = balance
        self.disabled: bool = disabled
        self.is_student: bool = is_student

    # Adding balance to the account, used for things like deposits
    def add_balance(self, amount: float, usable_in_session: bool = True):
        if amount <= 0:
            raise BankError(f'Amount must be positive')

        if self.balance + amount > BankAccount.MAXIMUM_BALANCE:
            raise BankError(f'Action would exceed the account balance limit of ${BankAccount.MAXIMUM_BALANCE}')

        if usable_in_session:
            self.usable += amount

        self.balance += amount


    # Deducting balance from the account, used for things like withdrawals and paying bills
    def deduct_balance(self, amount: float):
        if amount <= 0:
            raise BankError(f'Amount must be positive')

        if self.usable - amount < 0:
            raise BankError(f'Action would use more money than there is in the account')

        self.usable -= amount
        self.balance -= amount

# Account Holder Class, used for storing account holder information, [i.e. Standard User]
class AccountHolder:
    #Global Variable
    MAXIMUM_NAME_LENGTH = 20

    #Constructor
    def __init__(self, name: str):
        self.name = name
        self.accounts: list[BankAccount] = []

    #Getter, used to get the specific bank account
    def get_account(self, number) -> BankAccount:
        n = number

        # checks if the number is a string, converts it to a float if it is
        if isinstance(number, str):
            try:
                n = float(number)
            except ValueError:
                raise BankError('Invalid account number')

        # checks if the number matches any of the account numbers
        for account in self.accounts:
            if account.account_number == n:
                return account

        raise BankError('Invalid account number')