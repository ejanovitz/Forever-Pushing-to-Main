from abstract import StdTransaction
from .session import StdSession, AdminSession, LoggedOutSession

# Logout transaction class, used to logout of the system
class Logout(StdTransaction):
    #Constructor
    def __init__(self, session):
        super().__init__(session, None)

    # Perform the transaction
    def perform(self):
        if isinstance(self.session, StdSession) or isinstance(self.session, AdminSession):
            print("See you next time!")
            self.write_transactions()
        elif isinstance(self.session, LoggedOutSession):
            print("ERROR: Must login first")

    # Write the transactions to the transaction file
    def write_transactions(self):
        with open("./transaction.txt", "w") as file:
            for log in self.session.transaction_logs:
                file.write(log + "\n")
            file.write("00                      00000 00000.00   \n")
