from backend import backend
class FileHandler:
    def __init__(self):
        pass

    def  read_transactions(self, inpfile):
        with open(inpfile, newline='') as file:
            print(file)
            backend.transactions.append(file)


