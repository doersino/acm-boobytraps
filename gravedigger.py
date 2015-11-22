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

# initialize empty map of wall cells
map = [['x' for field in range(width)] for row in range(height)]

# add some empty cells
for i in xrange(1, width * height * 2):
    randomWidth = random.randint(0, width-1)
    randomHeight = random.randint(0, height-1)
    map[randomHeight][randomWidth] = 'o'

# add some traps
for i in trapDominationOrdering[::-1]:
    randomWidth = random.randint(0, width-1)
    randomHeight = random.randint(0, height-1)
    map[randomHeight][randomWidth] = i
    if random.random() < 0.2:
        break

# set start and end points
startX = 0
startY = 0
endX = width - 1
endY = height - 1
#startX = random.randint(0, width-1)
#startY = random.randint(0, height-1)
#endX = random.randint(0, width-1)
#while endX != startX:
#    endX = random.randint(0, width-1)
#endY = random.randint(0, height-1)
#while endY != startY:
#    random.randint(0, height-1)

# make sure that start and end aren't walls
if map[startY][startX] == 'x':
    map[startY][startX] = 'o'
if map[endY][endX] == 'x':
    map[endY][endX] = 'o'

# print map
print trapDominationOrdering
print str(width) + " " + str(height)
for i in map:
    print ''.join(i)
print str(startX) + " " + str(startY)
print str(endX) + " " + str(endY)
