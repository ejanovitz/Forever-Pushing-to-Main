import pytest
import tempfile
import os
from read import read_old_bank_accounts

def write_temp_file(content):
    """Helper function to create a temporary file with the given content."""
    temp = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
    temp.write(content)
    temp.close()
    return temp.name

# Loop coverage: enter 1 time + decision coverage for all positive cases
def test_valid_account_successfully_read():
    content = "12345 Macy May             A 12345.67 0123 SP\n"
    file_path = write_temp_file(content)
    accounts = read_old_bank_accounts(file_path)
    os.remove(file_path)
    assert len(accounts) == 1
    print(len(accounts[0]['account_number']))
    assert accounts[0]['account_number'] == '12345'
    assert accounts[0]['name'] == 'Macy May'
    assert accounts[0]['status'] == 'A'
    assert accounts[0]['balance'] == 12345.67
    assert accounts[0]['total_transactions'] == 123
    assert accounts[0]['plan'] == 'SP'

############## decision coverage: Negative cases #####################
def test_invalid_length_throws_error(capsys):
    content = "12345 Macy May             A 01234.56 0123 "  # invalid length for acc,o plan type
    file_path = write_temp_file(content)
    accounts = read_old_bank_accounts(file_path)
    os.remove(file_path)
    captured = capsys.readouterr()
    assert "ERROR: Fatal error - Line 1: Invalid length (43 chars, expected 45)" in captured.out
    assert len(accounts) == 0

def test_invalid_account_number_throws_error(capsys):
    content = "12X45 Macy May             A 01234.56 0123 SP\n"
    file_path = write_temp_file(content)
    accounts = read_old_bank_accounts(file_path)
    os.remove(file_path)
    captured = capsys.readouterr()
    assert "ERROR: Fatal error - Line 1: Account number must be 5 digits" in captured.out
    assert len(accounts) == 0

def test_invalid_status_throws_error(capsys):
    content = "12345 Macy May             X 01234.56 0123 SP\n"
    file_path = write_temp_file(content)
    accounts = read_old_bank_accounts(file_path)
    os.remove(file_path)
    captured = capsys.readouterr()
    assert "ERROR: Fatal error - Line 1: Invalid status 'X'. Must be 'A' or 'D'" in captured.out
    assert len(accounts) == 0

def test_negative_balance_throws_error(capsys):
    content = "12345 Macy May             A -1234.56 0123 SP\n"
    file_path = write_temp_file(content)
    accounts = read_old_bank_accounts(file_path)
    os.remove(file_path)
    captured = capsys.readouterr()
    assert "ERROR: Fatal error - Line 1: Negative balance detected: -1234.56" in captured.out
    assert len(accounts) == 0  # Negative balance should be rejected

def test_invalid_balance_format_throws_error(capsys):
    content = "12345 Macy May             A 12345,67 0123 SP\n"  # Comma instead of dot
    file_path = write_temp_file(content)
    accounts = read_old_bank_accounts(file_path)
    os.remove(file_path)
    captured = capsys.readouterr()
    assert "ERROR: Fatal error - Line 1: Invalid balance format. Expected XXXXX.XX, got 12345,67" in captured.out
    assert len(accounts) == 0

def test_invalid_transactions_throws_error(capsys):
    content = "12345 Macy May             A 01234.56 ABCD SP\n"  # Non-numeric transactions
    file_path = write_temp_file(content)
    accounts = read_old_bank_accounts(file_path)
    os.remove(file_path)
    captured = capsys.readouterr()
    assert "ERROR: Fatal error - Line 1: Transaction count must be 4 digits" in captured.out
    assert len(accounts) == 0

def test_invalid_plan_type_throws_error(capsys):
    content = "12345 Macy May             A 01234.56 0123 XX\n"  # Invalid plan type
    file_path = write_temp_file(content)
    accounts = read_old_bank_accounts(file_path)
    os.remove(file_path)
    captured = capsys.readouterr()
    assert "ERROR: Fatal error - Line 1: Invalid plan type 'XX'. Must be SP or NP" in captured.out  # Check error message
    assert len(accounts) == 0

# Loop coverage: enter multiple times
def test_multiple_valid_and_invalid_lines_reads_successfully_and_throws_errors(capsys):
    content = (
        "12345 Macy May             A 01234.56 0123 SP\n"  # Valid
        "12X45 Macy May             A 01234.56 0123 SP\n"  # Invalid account number
        "12345 Macy May             A -1234.56 0123 SP\n"  # Negative balance
        "56785 Alice Smith          D 00500.00 0005 NP\n"  # Valid
    )
    file_path = write_temp_file(content)
    accounts = read_old_bank_accounts(file_path)
    os.remove(file_path)
    captured = capsys.readouterr()
    print(captured)
    assert ("ERROR: Fatal error - Line 2: Account number must be 5 digits\n"
            "ERROR: Fatal error - Line 3: Negative balance detected: -1234.56") in captured.out
    assert len(accounts) == 2  # Only the valid ones should be included
    assert accounts[0]['account_number'] == '12345'
    assert accounts[1]['account_number'] == '56785'

# Loop coverage: enter 0 times
def test_empty_file():
    file_path = write_temp_file("")
    accounts = read_old_bank_accounts(file_path)
    os.remove(file_path)
    assert len(accounts) == 0
