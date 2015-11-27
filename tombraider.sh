#!/bin/bash

# Tests boobytraps.py with some input (if no input file is given,
# sampleinput.txt will be used) and optionally verifies the output.
# Additionally prints the time taken.
#
# Usage:
# ./test.sh [-i SAMPLE_INPUT [-o SAMPLE_OUTPUT]]

PY_FILE="boobytraps.py"
DEFAULT_INPUT="sampleinput.txt"
DEFAULT_OUTPUT="sampleoutput.txt"

# Process options
if [ "$1" = "-i" ]; then
	if [ -e "$2" ]; then
		INPUT="$(cat $2)"
	else
		INPUT="$2"
	fi

	if [ "$3" = "-o" ]; then
		if [ -e "$4" ]; then
			OUTPUT="$(cat $4)"
		else
			OUTPUT="$4"
		fi
	fi
else
	INPUT="$DEFAULT_INPUT"
	OUTPUT="$DEFAULT_OUTPUT"
fi

# Print expected input and output
printf "\e[1;34mEntering the following input:\e[0m\n"
echo "$INPUT"

if [ ! -z "$OUTPUT" ]; then
	printf "\e[1;34mExpecting the following output:\e[0m\n"
	echo "$OUTPUT"
fi

# Run script and verify output
printf "\e[1;34mRunning $PY_FILE:\e[0m\n"
if [ ! -z "$OUTPUT" ]; then
	if [ "$(echo "$INPUT" | time python "$PY_FILE")" = "$OUTPUT" ]; then
		printf "\e[1;32m+-----------------+\e[0m\n"
		printf "\e[1;32m| TEST SUCCESSFUL |\e[0m\n"
		printf "\e[1;32m+-----------------+\e[0m\n"
	else
		printf "\e[1;31m+-------------------+\e[0m\n"
		printf "\e[1;31m| TEST UNSUCCESSFUL |\e[0m\n"
		printf "\e[1;31m+-------------------+\e[0m\n"
		printf "\e[1;31mActual output:\e[0m\n"
		echo "$INPUT" | python "$PY_FILE" 2>/dev/null
		exit 1
	fi
else
	time python "$PY_FILE" < "$INPUT"
fi
