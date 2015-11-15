#!/bin/bash

# Tests boobytraps.py with some input (if none is given, sampleinput.txt will be
# used) and optionally verifies the output. Additionally prints the time taken.
#
# Usage:
# ./test.sh [-i SAMPLE_INPUT [-o SAMPLE_OUTPUT]]

PY_FILE="boobytraps.py"
DEFAULT_INPUT="sampleinput.txt"
DEFAULT_OUTPUT="sampleoutput.txt"

# Options processing
if [ "$1" = "-i" ]; then
	INPUT="$2"
	if [ "$3" = "-o" ]; then
		OUTPUT="$4"
	fi
else
	INPUT="$DEFAULT_INPUT"
	OUTPUT="$DEFAULT_OUTPUT"
fi

time python "$PY_FILE" < "$INPUT"

# TODO compare output
