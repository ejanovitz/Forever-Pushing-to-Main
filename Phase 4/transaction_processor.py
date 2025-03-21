# This is the transaction processor class, which will calculate the total cost of transactions.
class TransactionProcessor:
    # Constructor
    def __init__(self, ):
        self.file = None
    
    # This function calculates the total cost of transactions and returns a dict.
    def daily_cost_per_plan(self, transaction_file):
        # First, we need to open the file
        self.file = transaction_file
        transaction_dict = {'SP': 0.00, 'NP': 0.00}

        # Now, we have to write this
        with open(self.file, 'r') as file:
            # Parse each line
            for line in file:
                plan = line[-2:]
                if plan == 'SP':
                    transaction_dict['SP'] += 0.05
                else:
                    transaction_dict['NP'] += 0.10
        
        file.close()
        return transaction_dict
