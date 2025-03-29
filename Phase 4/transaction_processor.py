from logger import Logger

# This is the transaction processor class, which will calculate the total cost of transactions.
class TransactionProcessor:
    # Constructor
    def __init__(self):
        self.file = None
        self.logger = Logger()
    
    # This function calculates the total cost of transactions and returns a dict.
    def daily_cost_per_plan(self, transaction_file):
        # First, we need to open the file
        file = transaction_file
        transaction_dict = {'SP': 0.00, 'NP': 0.00}

        # Now, we have to read this file in order to do caluclations
        try: 
            with open(file, 'r') as file:
                # In order to calculate, we first read every line
                for line in file:
                    # Then, we get rid of potential white spaces
                    line = line.strip()
                    plan = line[-2:]

                    # Calculations
                    if plan == 'SP':
                        transaction_dict['SP'] = round(transaction_dict['SP'] + 0.05, 2)
                    elif plan == 'NP':
                        transaction_dict['NP'] = round(transaction_dict['NP'] + 0.10, 2)
        except FileNotFoundError:
            # Use class logger since this is a static method
            self.logger.log_error("File Error", "Transaction file not found", transaction_file)
        except Exception as e:
            # Log any other errors
            self.logger.log_error("Processing Error", str(e), transaction_file)
        
        file.close()
        return transaction_dict

