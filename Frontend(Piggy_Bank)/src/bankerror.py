# Bank Error Class, which raises an exception when an error occurs
class BankError(Exception):
    def __init__(self, message):
        super().__init__(message)