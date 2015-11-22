# Generate (large!) maps for testing boobytraps.py and write the result to
# stdout.
#
# Usage: gravedigger.py WIDTH HEIGHT

import argparse
import sys
import random

# parse options
parser = argparse.ArgumentParser()
parser.add_argument("width", metavar="WIDTH", type=int, choices=xrange(1, 40000), help="desired width of the map")
parser.add_argument("height", metavar="HEIGHT", type=int, choices=xrange(1, 40000), help="desired height of the map")
parser.add_argument("--seed", help="seed for map generation")
args = parser.parse_args()

if args.width * args.height > 40000:
    sys.exit("usage: " + __file__ + " [-h] WIDTH HEIGHT\n" + __file__ + ": error: WIDTH * HEIGHT must not exceed 40000")

if not args.seed:
    rand = random.SystemRandom()
    args.seed = rand.random()

# initialize random number generator
seed = args.seed
random.seed(seed)

# generate map
trapDominationOrdering = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
width = args.width
height = args.height
map = [['x' for field in range(width)] for row in range(height)]

#TODO fill map


# set start and end points, make sure they aren't walls
#TODO randomize
startX = 0
startY = 0
endX = width - 1
endY = height - 1
map[startY][startX] = 'o'
map[endY][endX] = 'o'

# print map
print trapDominationOrdering
print str(width) + " " + str(height)
for i in map:
    print ''.join(i)
print str(startX) + " " + str(startY)
print str(endX) + " " + str(endY)
