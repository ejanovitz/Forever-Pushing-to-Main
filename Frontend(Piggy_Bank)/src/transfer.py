from abstract import Transaction, StdTransaction, Session
from .session import AdminSession,StdSession


# Transfer transaction class, used to transfer money between accounts
class Transfer(StdTransaction):
    def __init__(self, session: Session):
        super().__init__(session, 2)
        self.transaction_num = "4"

    def perform(self):
        is_admin = isinstance(self.session, AdminSession)

        # Initialize total_transferred if not already set
        if not hasattr(self.session, "total_transferred"):
            setattr(self.session, "total_transferred", 0)

        total_transferred = self.session.total_transferred

        # Get source and destination accounts
        source_account_num = input("Enter the source account number: \n")
        dest_account_num = input("Enter the destination account number: \n")

        # Validate source account
        if not self._validate_account(source_account_num, "source"):
            return

        # For non-admin users, ensure the source account belongs to the current user
        if not is_admin and not self._is_account_owned_by_user(source_account_num):
            print("Error: You can only transfer funds from your own accounts.")
            return

        # Validate destination account
        if not self._validate_account(dest_account_num, "destination"):
            return

        # Check if source and destination accounts are the same
        if source_account_num == dest_account_num:
            print("Error: Source and destination accounts cannot be the same.")
            return

        # Get transfer amount
        if is_admin:
            amount = self.session.input_positive_money(99999.99)
        else:
            max_available = 1000.00 - total_transferred
            self.session.total_transferred = max_available
            amount = self.session.input_positive_money(max_available)

        # Confirm transfer
        confirm = input('Do you want to proceed? (Y/n): \n').strip().lower()
        if confirm != 'y':
            print("Transfer canceled.")
            return

        # Perform transfer
        if self.transfer_funds(source_account_num, dest_account_num, amount):
            print(f"Transferred ${amount:.2f} from account {source_account_num} to account {dest_account_num}.\n")
            
            # Get the actual account objects
            source_account = self._get_account(source_account_num)
            dest_account = self._get_account(dest_account_num)
            
            # Log the transaction with both accounts
            self.log(amount, source_account, dest_account)
        else:
            print("Transfer failed. Please check the account numbers and balances.")
            
    def log(self, amount, source_account, dest_account, tags='TF'):
        """
        Logs the transfer transaction with two lines:
        1. Transferer (source account) with transaction number.
        2. Transferee (destination account) without transaction number.
        The first character of each username is aligned.
        """
        # Format the transferer's line
        transferer_name = f"{source_account.account_holder.name:<20}"  # Left-align the name to 20 characters
        transferer_log = f"0{self.transaction_num} {transferer_name} {source_account.account_number:05} {amount:08.2f} {tags}"
        
        # Format the transferee's line
        transferee_name = f"{dest_account.account_holder.name:<20}"  # Left-align the name to 20 characters
        transferee_log = f"   {transferee_name} {dest_account.account_number:05} {amount:08.2f}"
        
        # Append both lines to the transaction logs
        self.session.transaction_logs.append(transferer_log)
        self.session.transaction_logs.append(transferee_log)

    def transfer_funds(self, source_account, dest_account, amount):
        try:
            # Check if accounts are disabled
            if self._is_account_disabled(source_account) or self._is_account_disabled(dest_account):
                return False

            # Deduct from source account
            source_balance = self._get_account_balance(source_account)
            if source_balance is None or source_balance < amount:
                print("Error: Insufficient funds in the source account.")
                return False

            # Add to destination account
            dest_balance = self._get_account_balance(dest_account)
            if dest_balance is None:
                return False

            # Update balances
            self._update_account_balance(source_account, source_balance - amount)
            self._update_account_balance(dest_account, dest_balance + amount)
            return True
        except Exception as e:
            print(f"Error during transfer: {e}")
            return False

    def _validate_account(self, account_number: str, account_type: str) -> bool:
        account = self._get_account(account_number)
        if not account:
            print(f"Error: {account_type.capitalize()} account not found.")
            return False
        if account.disabled:
            print(f"Error: {account_type.capitalize()} account is disabled.")
            return False
        return True



    def _is_account_owned_by_user(self, account_number: str) -> bool:
        """
        Standard users should only be able to transfer from their own accounts.
        """
        if isinstance(self.session, AdminSession):
            return True
        
        # Ensure user can only use their own accounts as the source
        for account in self.session.account_holder.accounts:
            if account.account_number == int(account_number):
                return True
        
        print(f"Error: Account {account_number} does not belong to {self.session.account_holder.name}")
        return False


    def _get_account(self, account_number: str, source=False):
        """
        Retrieves an account, restricting standard users from using others' accounts as source.
        """
        try:
            account_number = int(account_number)
            
            # Standard users can only use their own accounts as source
            if isinstance(self.session, StdSession) and source:
                for account in self.session.account_holder.accounts:
                    if account.account_number == account_number:
                        return account
                print(f"Error: Standard user cannot use account {account_number} as source")
                return None
            
            # Admins and all users can transfer to any valid destination
            if self.session.bank_ui:
                for account_holder in self.session.bank_ui.account_holders:
                    for account in account_holder.accounts:
                        if account.account_number == account_number:
                            return account
            
            print(f"Error: Account {account_number} not found")
            return None
        except ValueError:
            print("Error: Invalid account number format")
            return None

    def _is_account_disabled(self, account_number: str) -> bool:
        """
        Ensure the correct account object is checked for its disabled status.
        """
        account = self._get_account(account_number)
        if account is None:
            print(f"Error: Cannot check disabled status, account {account_number} not found.")
            return True  # Assume disabled if not found
        
        return account.disabled

    def _get_account_balance(self, account_number: str) -> float:
        account = self._get_account(account_number)
        return account.balance if account else None

    def _update_account_balance(self, account_number: str, new_balance: float) -> bool:
        account = self._get_account(account_number)
        if account:
            account.balance = new_balance
            account.usable = new_balance
            return True
        return False