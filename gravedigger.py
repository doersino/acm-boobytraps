# Generate (large!) maps for testing boobytraps.py and write the result to
# stdout.
#
# Usage: gravedigger.py WIDTH HEIGHT

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("width", metavar="WIDTH", type=int, help="desired width of the map")
parser.add_argument("height", metavar="HEIGHT", type=int, help="desired height of the map")
args = parser.parse_args()

print args.width
print args.height
