from .session import AdminSession, StdSession
from .account import AccountHolder, BankAccount
from .login import Login
from .logout import Logout
from .withdrawal import Withdrawal
from .transfer import Transfer
from .paybill import Paybill
from .deposit import Deposit
from .create import Create
from .delete import Delete
from .disable import Disable
from .changeplan import Changeplan
from .bankerror import BankError

# The front-end class that interacts with the user
class BankUI:
    # Constructor
    def __init__(self):
        self.session = None
        self.account_holders = []
        self.loaded = False

    # Used to get account information, useful for both admin and standard users
    # Standard is useful if they have more accounts, as it initializes the first one during login.
    def parse_account_line(self, line):
        if not line.strip():
            return None
        return {
            'number': int(line[0:5]),  # Account number (columns 0-5)
            'name': line[6:26].strip(),  # Account holder name (columns 6-26)
            'balance': float(line[29:37]),  # Account balance (columns 29-37)
            'disabled': line[27] == 'D'  # Disabled status (column 27)
        }

    def get_account_holder(self, name: str):
        for holder in self.account_holders:
            if holder.name == name:
                return holder
        raise BankError('Invalid account holder name')
    
    # Loads all the accounts from the bank_account.txt file to the bank UI session
    
    def load_accounts(self):
        if isinstance(self.session, StdSession):
            self.account_holders.append(self.session.account_holder)

        if not self.loaded:
            try:
                with open("./bank_account.txt", "r") as file:
                    bank_account = file.readlines()

                for line in bank_account:
                    account_data = self.parse_account_line(line)
                    if not account_data:
                        continue
                    
                    holder = next((h for h in self.account_holders if h.name == account_data["name"]), None)
                    if holder is None:
                        holder = AccountHolder(account_data['name'])
                        self.account_holders.append(holder)
                    
                    # Prevent duplicate account entries
                    existing_account = next((acc for acc in holder.accounts if acc.account_number == account_data['number']), None)
                    if existing_account is None:
                        account = BankAccount(
                            account_holder=holder,
                            account_number=account_data['number'],
                            balance=account_data['balance'],
                            disabled=account_data['disabled'],
                            is_student=False
                        )
                        holder.accounts.append(account)
                    
                    # Only add accounts belonging to the standard user (avoid duplicates)
                    if isinstance(self.session, StdSession) and holder.name == self.session.account_holder.name:
                        user_existing_account = next((acc for acc in self.session.account_holder.accounts if acc.account_number == account_data['number']), None)
                        if user_existing_account is None:
                            self.session.account_holder.accounts.append(account)

                    # Populate AdminSession's accounts list
                    if isinstance(self.session, AdminSession):
                        self.session.accounts.append(account)

                self.loaded = True
            except FileNotFoundError:
                print("Error: Bank account file not found")
                return False
            except (ValueError, IndexError):
                print("Error: Invalid Username")
                return False
        return True



    def print_welcome_message(self):
        #Print Welcome Message
        current_session = self.session
        if isinstance(self.session, AdminSession):
            return
        print(f"Welcome {current_session.account_holder.name}")
        print("== Accounts ==")

        # Goes through and prints all the accounts
        if isinstance(self.session, AdminSession):
            for account in current_session.accounts:
                print(f"{account.account_number:05d}    {account.account_holder.name:<20}  Account Balance: ${account.balance:.2f}")
        else:
            for account in self.session.account_holder.accounts:
                print(f"{account.account_number:05d} {'D' if account.disabled else 'A'} ${account.balance:.2f}")

    
    #Run the front end UI
    def run(self):
        # Initialize Program and print message to user
        running = True
        while running:
            # Use this variable to access rest of the program
            has_logged_in = False
            while not has_logged_in:
                print("Welcome to the Big Bank!")
                transaction = input("Please enter a transaction: \n")

                #you can only login or exit at this point
                if transaction == "login":
                    login = Login(self)
                    self.session, has_logged_in = login.perform()
                    if self.session == None:
                        continue
                    if not self.load_accounts():
                        return
                    self.print_welcome_message()
                elif transaction == "exit":
                    return
                else:
                    print("Error: Invalid transaction")
                    if transaction == ' ':
                        return

            #Has logged in
            while has_logged_in:
                try:
                    # Transaction Prompt
                    transaction = input("Please enter a transaction: \n")
                    
                    if transaction == "logout":
                        logout = Logout(self.session)
                        logout.perform()
                        has_logged_in = False
                        running = False
                    elif transaction == "withdrawal":
                        withdrawal = Withdrawal(self.session)
                        withdrawal.perform()
                    elif transaction == "transfer":
                        transfer = Transfer(self.session)
                        transfer.perform()
                    elif transaction == "paybill":
                        paybill = Paybill(self.session)
                        paybill.perform()
                        self.print_welcome_message()
                    elif transaction == "deposit":
                        deposit = Deposit(self.session)
                        deposit.perform()
                    elif transaction == "create":
                        create = Create(self.session)
                        create.perform()
                    elif transaction == "delete":
                        delete = Delete(self.session)
                        delete.perform()
                    elif transaction == "disable":
                        disable = Disable(self.session)
                        disable.perform()
                    elif transaction == "changeplan":
                        changeplan = Changeplan(self.session)
                        changeplan.perform()
                    elif transaction == "login":
                        print("You're already logged in!")
                        self.print_welcome_message()
                    else:
                        print("Error: Invalid transaction")
                except BankError as ex:
                    print(f'Error: {ex}')
