#!/bin/bash
# weekly.sh – Weekly script for running Front End sessions, merging transaction files,
#           and invoking the Back End.
# Run this script from inside the Frontend(Piggy_Bank) directory.

# Create (or re-create) the output directory and remove any prior output files.
mkdir -p weekly_output
rm -rf weekly_output/day_*
rm -f merged_transactions.txt

# (Optional) Back up the original bank account file.
cp bank_account.txt current_bank_accounts.txt

# For this, we have to create a new directory every week

for i in {1..7}; do
    echo "=== Big Bank - Day $i ==="
    mkdir -p weekly_output/day_$i
    # Process each session file in the sessions folder.
    for session_file in sessions/*.txt; do
        session_name=$(basename "$session_file" .txt)
        echo "▶ Running session: $session_name"

        # Run the Front End using main.py and feed in the session file.
        # The Front End should write its transaction output to "transaction.txt" upon logout.
        python3 main.py < "$session_file"

        # Pause briefly to allow the file to be fully written.
        sleep 1

        # Debug: List the file if found.
        if [ -f transaction.txt ]; then
            echo "Found transaction.txt after $session_name:"
            ls -l transaction.txt

            # Immediately move the file so the next session doesn't overwrite it.
            mv transaction.txt "weekly_output/day_${i}/${session_name}.etf"
            echo "Saved: weekly_output/day_${i}/${session_name}.etf"
        else
            echo "Warning: transaction.txt not found after $session_name"
    #        echo "Listing current directory for debugging:"
    #        ls -la
        fi
    done

    # Merge all individual session files into one merged transaction file.
    cat weekly_output/day_$i/*.etf > merged_transactions.txt
    echo "Merged daily transaction files into merged_transactions.txt"

    # Move to the Backend directory and run the backend file.
    cd ../Backend && python3 backend.py
    sleep 1

    #Change frontend bank accounts to the new one
    cat new_current_file.txt > ../'Frontend(Piggy_Bank)'/current_bank_accounts.txt
    echo "Updated current bank accounts from the Back End."

    # Move back to the Frontend directory.
    cd ../'Frontend(Piggy_Bank)'

    echo "Daily run complete."
done

echo "Weekly run complete."
