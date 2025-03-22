from abstract import Transaction
from .session import AdminSession, StdSession
from .account import AccountHolder, BankAccount

# Login class, used to login to the system
class Login(Transaction):
    # Constructor
    def __init__(self, bank_ui):
        super().__init__(None, None)
        self.bank_ui = bank_ui
    
    # Perform the login
    def perform(self):
        try:
            # Get the user type
            ses = input('Are you a [standard] or [admin] user: \n').lower().strip()
            if ses == 'admin':
                # Create the admin session
                self.session = AdminSession(bank_ui=self.bank_ui)
                return self.session, True
            elif ses == 'standard':
                # Get the username
                name = input('Please enter your username: \n').strip()

                # Checks if the username is valid and creates the standard session
                try:
                    with open("./bank_account.txt", "r") as file:
                        account_lines = file.readlines()
                        
                    # Find the matching account line
                    matching_line = None
                    for line in account_lines:
                        if line[6:25].strip() == name:
                            matching_line = line
                            break

                    if matching_line is None:
                        print('Error: Invalid Username')
                        return None, False

                    # Create account holder and account, since for standard users, we need one
                    # This will be simplified in future versions
                    holder = AccountHolder(name)
                    account_number = int(matching_line[0:5])
                    balance = float(matching_line[29:37])
                    disabled = matching_line[27:28] == 'D'
                    account = BankAccount(
                        account_holder=holder,
                        account_number=account_number,
                        balance=balance,
                        disabled=disabled,  # Default value
                        is_student=False  # Default value
                    )
                    holder.accounts.append(account)
                    self.session = StdSession(holder, self.bank_ui)  # Pass bank_ui here
                    return self.session, True

                except FileNotFoundError:
                    print('Error: Bank account file not found')
                    return None, False
                except (ValueError, IndexError):
                    print('Error: Invalid Username')
                    return None, False
            else:
                print("Error: Expected 'standard' or 'admin'")
                return None, False
                
        except Exception as e:
            print(f'Error: An unexpected error occurred - {str(e)}')
            return None, False