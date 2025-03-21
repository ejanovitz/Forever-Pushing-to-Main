from file_handler import FileHandler
class backend:

    # Declaring global arrays to store transactions and accounts for reading and writing to files
    transactions = []
    accounts = []
    def main():
        FileHandler = FileHandler()

        FileHandler.read_file('master_file.txt')
