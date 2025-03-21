from file_handler import FileHandler 

def main():

    # Populate transactions array
    FileHandler.read_transactions("merged_transactions.txt")
    #Populate accounts array
    FileHandler.read_old_bank_account_file("master_file.txt")

main()
