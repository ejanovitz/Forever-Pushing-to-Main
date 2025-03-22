from abstract import StdTransaction
from .session import StdSession
from .bankerror import BankError

# Withdrawal transaction class, used to withdraw money from an account
class Withdrawal(StdTransaction):
    #Constructor
    def __init__(self, session):
        super().__init__(session, 1)

    # Perform the transaction
    def perform(self):
        account = self.session.input_local_account('What account holder will be withdrawn from', 'Which account number will be withdrawn from')
        amount = self.session.input_positive_money(99999.99, 'How much will be withdrawn')
        

        try:
            if isinstance(self.session, StdSession):
                if (self.session.amount_withdrawn or 0) + amount > 500:
                    raise BankError('Withdrawal would exceed $500.00 session limit')

                self.session.amount_withdrawn = (self.session.amount_withdrawn or 0) + amount

            account.deduct_balance(amount)
            print(f'${amount:.2f} withdrawn from account {account.account_number}, balance: ${account.balance:.2f}')
            self.log(amount, account, '')
            
        except TypeError:
            pass
        except BankError as e:
            print(f"Error: {e}")

