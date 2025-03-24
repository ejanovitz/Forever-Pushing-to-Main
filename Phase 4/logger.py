class Logger:
    def __init__(self):
        self.log_file = 'log.txt'

    def log_error(self, error_type, description, file):
        error_msg = f"ERROR: {error_type}: {description} in file: {file}"
        print(error_msg)

    #Prints an error message for failed constraints in the required format
    def log_constraint_error(constraint_type, description):
        print(f"ERROR: {constraint_type}: {description}")