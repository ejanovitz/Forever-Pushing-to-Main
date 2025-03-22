# This is the transaction processor class, which will calculate the total cost of transactions.
class TransactionProcessor:
    # Constructor
    def __init__(self):
        self.file = None
    
    # This function calculates the total cost of transactions and returns a dict.
    def daily_cost_per_plan(self, transaction_file):
        # First, we need to open the file
        self.file = transaction_file
        transaction_dict = {'SP': 0.00, 'NP': 0.00}

        # Now, we have to read this file in order to do caluclations
        with open(self.file, 'r') as file:
            # In order to calculate, we first reead every line
            for line in file:
                # Then, we get rid of potential white spaces
                line = line.strip()
                plan = line[-2:]

                # Calculations
                if plan == 'SP':
                    transaction_dict['SP'] += 0.05
                else:
                    transaction_dict['NP'] += 0.10
        
        file.close()
        return transaction_dict
