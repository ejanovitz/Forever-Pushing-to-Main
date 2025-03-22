from abstract import Transaction, StdTransaction
from .account import BankAccount, AccountHolder
from .session import AdminSession
from .bankerror import BankError

# Paybill transaction class, this can be used to pay bills
class Paybill(StdTransaction):
    #Constructor
    def __init__(self, session):
        super().__init__(session, 3)

    # Perform the transaction
    def perform(self):
        # Check if the account exists
        if isinstance(self.session, AdminSession):
            account_name = input("Please type in the account holder's name: \n")
            account = input("Please type in their account number: \n")

            # parse the account line from bank account.txt to check if the account exists
            parsed_account = ''
            with open("./bank_account.txt", "r") as file:
                account_lines = file.readlines()
            for line in account_lines:
                if line[6:25].strip() == account_name and line[0:5] == account:
                    parsed_account = line
                    break
            
            if account_name == '' or account == '' or parsed_account[27:28] == 'D':
                print('Sorry, that account has been deactivated or invalid. Please try again.')
                return
            
            # Create an account object for the admin
            account = BankAccount(
                account_holder=AccountHolder(account_name),
                account_number=int(account),
                balance=float(parsed_account[29:37]),
                disabled=parsed_account[27:28] == 'D',
                is_student=False
            )

        else:
            account = input("Please type in your account number: \n")
            account_numbers = [acc.account_number for acc in self.session.account_holder.accounts]
            if int(account) not in account_numbers:
                print('Error: Invalid account number. Please try again.')
                return
            account = self.session.account_holder.get_account(account)
        
        #Check if the company they want to pay to is valid.
        if isinstance(self.session, AdminSession):
            company = input('Please type in the two character company code that they want to pay to: \n')
        else:
            company = input('Please type in the two character company code that you want to pay to: \n')
        if len(company) != 2 or company not in ['EC', 'CQ', 'FI']:
            print('Error: Invalid company code/name, please try again.')
            return

        #Check if the amount they want to pay is valid
        try:
            if isinstance(self.session, AdminSession):
                amount = self.session.input_positive_money(99999.99)
            else:
                amount = self.session.input_positive_money(2000.00)
            if amount == None:
                return

            #Confirmation
            confirm = input('Do you want to proceed? Y/n: \n')
            if confirm.lower() != 'y':
                print('Payment cancelled!\n')
                return

            # Process the payment
            account.deduct_balance(float(amount))
            self.log(amount, account, company)
            print(f'Payment sent! Remaining balance: ${account.balance:.2f}\n')

        except BankError as e:
            print(f'Error: {str(e)}')
            return

    # Log the transaction
    def log(self, amount, account='     ', tags='  '):
        # add to the session's transaction logs
        self.session.transaction_logs.append(f"0{self.transaction_num} {account.account_holder.name:20} {account.account_number:05} {amount:08.2f} {tags}")