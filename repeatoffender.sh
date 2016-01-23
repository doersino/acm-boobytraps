#!/bin/bash

# Feeds randomly generated square maps (using gravedigger.py) of all side lengths
# from 1 to 200 into boobytraps.py, measures the runtime, and outputs the
# results to stdout as well as a semicolon-separated CSV file.
#
# Usage: ./repeatoffender.sh [-n NUMBER_OF_SAMPLES] [-o OUTPUT_FILENAME]
#
#        Any other options are passed on to gravedigger.py.
#
# Examples: ./repeatoffender.sh -n 100
#           ./repeatoffender.sh -n 5 -o test.csv --complexity 12 --mode dungeon

# Process options
N=10
OUTPUTFILE="repeatoffender.csv"
GRAVEDIGGER_OPTIONS=""

while [[ $# > 0 ]]; do
    case $1 in
        -n)
        N="$2"
        shift
        ;;
        -o)
        OUTPUTFILE="$2"
        shift
        ;;
        *)
        GRAVEDIGGER_OPTIONS+=" $1"
        ;;
    esac
    shift
done

# Sanity checking
printf "\e[1mRunning \"./gravedigger.py --start 0,0 --end [WIDTH - 1],[HEIGHT - 1] $GRAVEDIGGER_OPTIONS [WIDTH] [HEIGHT] | ./boobytraps.py\" $N times for each WIDTH, HEIGHT in 1..200 and writing the result to \"$OUTPUTFILE\":\e[0m\n"

# Set up the time utility
TIMEFORMAT=%R

# Write row of column titles
echo "Map width/height; Number of map cells (i.e. width * height); Number of samples; Total time taken (in s); Time taken per sample (i.e. total time taken / number of samples, in s); Time taken per sample (in ms)" | tee /dev/tty | cat > "$OUTPUTFILE"

for WH in {1..200}; do
    SE="$(expr $WH - 1)"

    # Run benchmark for current map width and height
    TIME=$({ time for ((i = 1; i <= $N; i++)); do ./gravedigger.py --start 0,0 --end $SE,$SE $GRAVEDIGGER_OPTIONS $WH $WH | ./boobytraps.py >/dev/null; done; } 2>&1)

    # Compute remaining columns
    WHSQ="$(bc <<< "$WH * $WH")"
    TIMEPERSAMPLE="$(bc <<< "scale=8; $TIME / $N")"
    TIMEPERSAMPLEMS="$(bc <<< "$TIMEPERSAMPLE * 1000")"

    # Write row
    echo "$WH; $WHSQ; $N; $TIME; $TIMEPERSAMPLE; $TIMEPERSAMPLEMS" | tee /dev/tty | cat >> "$OUTPUTFILE"
done
