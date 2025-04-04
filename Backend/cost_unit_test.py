import pytest
import os
import re
from transaction_processor import TransactionProcessor  # Adjust import as needed


@pytest.fixture
def create_test_file(tmp_path):
    """Helper function to create a temporary file with the given content."""

    def _create_file(filename, lines):
        file_path = tmp_path / filename
        with open(file_path, "w") as f:
            for line in lines:
                f.write(line + "\n")
        return str(file_path)  # return the string path
    return _create_file


def test_daily_cost_empty_file(create_test_file):
    """
    Tests that an empty file returns {'SP': 0.0, 'NP': 0.0}.
    This ensures the loop is executed zero times.
    """
    # Create an empty file
    test_file = create_test_file("empty_file.txt", [])

    tp = TransactionProcessor()

    result = tp.daily_cost_per_plan(test_file)
    assert result == {'SP': 0.0, 'NP': 0.0}, "Expected empty file to produce zero costs"


def test_daily_cost_sp_only(create_test_file):
    """
    Tests multiple lines ending with 'SP' only.
    Ensures we hit the if plan == 'SP' branch.
    """
    lines = ["Acct00001 SP", "Acct00002 SP", "OtherStuff SP"]
    test_file = create_test_file("sp_file.txt", lines)

    tp = TransactionProcessor()

    result = tp.daily_cost_per_plan(test_file)
    # 3 lines each adds $0.05 to SP
    assert result["SP"] == 0.15
    assert result["NP"] == 0.0


def test_daily_cost_np_only(create_test_file):
    """
    Tests multiple lines ending with 'NP' only.
    Ensures we hit the elif plan == 'NP' branch.
    """
    lines = ["Acct10001 NP", "Acct10002 NP"]
    test_file = create_test_file("np_file.txt", lines)

    tp = TransactionProcessor()

    result = tp.daily_cost_per_plan(test_file)
    # 2 lines each adds $0.10 to NP
    assert result["SP"] == 0.0
    assert result["NP"] == 0.20


def test_daily_cost_mixed_plans(create_test_file):
    """
    Tests lines that end in SP and NP and also lines that end in something else
    to ensure we do NOT increment for lines that are neither 'SP' nor 'NP'.
    """
    lines = [
        "Acct20001 SP",
        "Acct20002 NP",
        "SomethingXX",  # Not SP or NP, so no increment
        "Acct20003 SP"
    ]
    test_file = create_test_file("mixed_file.txt", lines)

    tp = TransactionProcessor()

    result = tp.daily_cost_per_plan(test_file)
    # SP lines: 2 => 2 * 0.05 = 0.10
    # NP lines: 1 => 1 * 0.10 = 0.10
    assert result["SP"] == 0.10
    assert result["NP"] == 0.10


def test_daily_cost_file_not_found(capsys):
    """
    Tests FileNotFoundError path by passing a filename that doesn't exist.
    This should trigger the FileNotFoundError exception block.
    """
    fake_file = "no_such_file.txt"
    tp = TransactionProcessor()

    # For this, we can assume it crashes the program. So, we call pytest.raises
    with pytest.raises(SystemExit):
        result = tp.daily_cost_per_plan(fake_file)

    # Here, we have to capture the output and compare.
    captured = capsys.readouterr()
    expected_output = "ERROR: File Error: Transaction file not found in file: no_such_file.txt"
    assert expected_output in captured.out


def test_daily_cost_general_exception(tmp_path, capsys):
    """
    Tests the generic exception block by passing a directory instead of a file path.
    On some systems, attempting to open a directory throws IsADirectoryError,
    which is caught by the general exception handler.
    """
    dir_path = tmp_path  # This is a directory
    tp = TransactionProcessor()

    # For this, we can assume it crashes the program. So, we call pytest.raises
    with pytest.raises(SystemExit):
        result = tp.daily_cost_per_plan(str(dir_path))

    # Capture the output for this
    captured = capsys.readouterr()

    #Compares regex of expected pattern vs output
    expected_pattern = re.compile(
        r"ERROR: Processing Error: .+ in file: " + re.escape(str(dir_path)))
    assert expected_pattern.search(captured.out)
