from abstract import Transaction, StdTransaction
from .bankerror import BankError
# Deposit transaction class, used to deposit money into an account
class Deposit(StdTransaction):
    #Constructor
    def __init__(self, session):
        super().__init__(session, 4)

    # Perform the transaction
    def perform(self):
        account = self.session.input_local_account('What account holder will be deposited to', 'Which account number will be deposited to')
        amount = self.session.input_positive_money(99999.99, 'How much will be deposited')
        
        try:
            # adds the balance to the account
            account.add_balance(amount, False)
            print(f'${amount:.2f} deposited to account' 
                  + f' {account.account_number},'
                  + f' balance: ${account.balance:.2f}, usable: ${account.usable:.2f}')
            self.log(amount, account, '')
        except TypeError:
            pass
        except BankError as e:
            print(f"Error: {e}")