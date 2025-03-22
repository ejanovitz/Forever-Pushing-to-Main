#!/bin/bash

REGRESSION_TESTS=("deposit" "withdrawal" "create", "logout", "delete", "disable", "changeplan")

SUBSTRING=()
RUN_ALL=""

while [ $# -gt 0 ]
do
    case $1 in
        -a)
            RUN_ALL="true"
            shift
            ;;
        -r)
            SUBSTRING+=( "${REGRESSION_TESTS[@]}" )
            shift
            ;;
        -*)
            echo Unrecognized argument $1
            exit 2
            ;;
        *)
            SUBSTRING+=($1)
            shift
            ;;
    esac
done

TESTS_DIR=tests
STDOUT_FILE=$(mktemp)
TRANSACTIONS_OUTPUT_FILE=transaction.txt
COMMAND=./main.py

DIFF_FILE=$(mktemp)

TOTAL_TESTS=0
FAILED_TESTS=0

INPUT_FILE=input.txt
OUTPUT_FILE=output.txt
TRANSACTIONS_FILE=transactions.txt

function run_test() {
    TEST_CATEGORY=$1
    TEST_NAME=$2
    TEST="$TESTS_DIR"/"$TEST_CATEGORY"/"$TEST_NAME"

    echo > "$TRANSACTIONS_OUTPUT_FILE"
    cat "$TEST"/"$INPUT_FILE" | python3 "$COMMAND" > "$STDOUT_FILE"

    if ! diff -Z --color=always -U1000 "$TEST"/"$OUTPUT_FILE" $STDOUT_FILE > "$DIFF_FILE" \
        || ! diff -Z --color=always -U1000 "$TEST"/"$TRANSACTIONS_FILE" "$TRANSACTIONS_OUTPUT_FILE" > "$DIFF_FILE"
    then
        echo Test failed: "$TEST_NAME"
        cat "$DIFF_FILE"
        if [ "$RUN_ALL" != "true" ]
        then
            exit 1
        fi
        echo
        echo

        FAILED_TESTS=$(("$FAILED_TESTS" + 1))
    fi

    TOTAL_TESTS=$(("$TOTAL_TESTS" + 1))
}

for TEST_CATEGORY in $(ls "$TESTS_DIR"/)
do
    if [ -d "$TESTS_DIR"/"$TEST_CATEGORY" ]
    then
        echo Testing category "$TEST_CATEGORY"
        for TEST in $(ls "$TESTS_DIR"/"$TEST_CATEGORY")
        do
            SHOULD_RUN=false
            for I in "${SUBSTRING[@]}"
            do
                case "$TEST_CATEGORY"/"$TEST" in
                    *"$I"*)
                        SHOULD_RUN="true"
                        ;;
                esac
            done

            if [ "${#SUBSTRING[@]}" -eq 0 ] || [ "$SHOULD_RUN" = "true" ]
            then
                run_test $TEST_CATEGORY $TEST
            fi
        done
    fi
done

echo Testing finished!
echo "$FAILED_TESTS" tests failed out of "$TOTAL_TESTS" total
if [ "$FAILED_TESTS" -eq 0 ] && [ "$TOTAL_TESTS" -ne 0 ]
then
    echo "Good job!"
fi

