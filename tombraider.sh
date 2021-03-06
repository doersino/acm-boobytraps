#!/usr/bin/env bash

# Tests boobytraps.py with some input (if no input or input file is given,
# sampleinput.txt will be used) and optionally verifies the output.
# Additionally prints the time taken.
#
# Usage: ./tombraider.sh [-i SAMPLE_INPUT [-o SAMPLE_OUTPUT]]
#
# Examples: ./tombraider.sh -i sampleinput.txt -o sampleoutput.txt
#           ./tombraider.sh -i sampleinput2.txt -o 2

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
	INPUT="$(cat $DEFAULT_INPUT)"
	OUTPUT="$(cat $DEFAULT_OUTPUT)"
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
		printf "\e[1;32m+-----------------+\e[0m\n"  # green
		printf "\e[1;32m| TEST SUCCESSFUL |\e[0m\n"
		printf "\e[1;32m+-----------------+\e[0m\n"
	else
		printf "\e[1;31m+-------------------+\e[0m\n"  # red
		printf "\e[1;31m| TEST UNSUCCESSFUL |\e[0m\n"
		printf "\e[1;31m+-------------------+\e[0m\n"
		printf "\e[1;31mActual output (with the -v flag):\e[0m\n"
		echo "$INPUT" | python "$PY_FILE" -v 2>/dev/null
		exit 1
	fi
else
	echo "$INPUT" | time python "$PY_FILE" -v
fi
