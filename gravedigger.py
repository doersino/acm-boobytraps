# Generate (large!) maps for testing boobytraps.py and write the result to
# stdout.
#
# Usage: gravedigger.py WIDTH HEIGHT

import argparse
import sys
import random
import math

# parse options
parser = argparse.ArgumentParser()
parser.add_argument("width", metavar="WIDTH", type=int, choices=xrange(1, 40001), help="desired width of the map")
parser.add_argument("height", metavar="HEIGHT", type=int, choices=xrange(1, 40001), help="desired height of the map")
parser.add_argument("--seed", help="seed for random number generator used during map generation")
parser.add_argument("--mode", choices=["random", "dungeon"], help="random (default) or dungeon (with corridors and rooms)")
args = parser.parse_args()

if args.width * args.height > 40000:
    sys.exit("usage: " + __file__ + " [-h] WIDTH HEIGHT\n" + __file__ + ": error: WIDTH * HEIGHT must not exceed 40000")

if not args.seed:
    rand = random.SystemRandom()
    args.seed = rand.random()

if not args.mode:
    args.mode = "random"

# initialize random number generator
seed = args.seed
random.seed(seed)

# generate map
trapDominationOrdering = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
width = args.width
height = args.height

# initialize empty map of wall cells
map = [['x' for field in range(width)] for row in range(height)]

# switch between map generation modes
mode = args.mode

# normal map generation algorithm
if mode == "random":
    # add some empty cells
    for i in xrange(1, width * height * 2):
        randomX = random.randint(0, width-1)
        randomY = random.randint(0, height-1)
        map[randomY][randomX] = 'o'

    # add some traps
    for i in trapDominationOrdering[::-1]:
        randomX = random.randint(0, width-1)
        randomY = random.randint(0, height-1)
        map[randomY][randomX] = i
        if random.random() < 1 / math.sqrt(width * height):
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

# dungeon map generation algorithm
elif mode == "dungeon":
    # add some corridors
    # horizontal
    for i in xrange(1, int(math.floor((width + height) / 4))):
        randomX = random.randint(0, width-1)
        randomY = random.randint(0, height-1)
        randomRadius = random.randint(1, math.floor((width-1) / 2))
        randomXStart = max(0, min(width-1, randomX - randomRadius - 1))
        randomXStop = max(0, min(width-1, randomX + randomRadius))
        for x in xrange(randomXStart, randomXStop + 1):
            map[randomY][x] = 'o'

    # vertical
    for i in xrange(1, int(math.floor((width + height) / 4))):
        randomX = random.randint(0, width-1)
        randomY = random.randint(0, height-1)
        randomRadius = random.randint(1, math.floor((height-1) / 2))
        randomYStart = max(0, min(height-1, randomY - randomRadius - 1))
        randomYStop = max(0, min(height-1, randomY + randomRadius))
        for y in xrange(randomYStart, randomYStop + 1):
            map[y][randomX] = 'o'

    # add some random empty cells
    for i in xrange(1, width + height):
        randomX = random.randint(0, width-1)
        randomY = random.randint(0, height-1)
        map[randomY][randomX] = 'o'

    # add some traps: no traps wanted in rooms
    for i in trapDominationOrdering[::-1]:
        while random.random() < .5:
            randomX = random.randint(0, width-1)
            randomY = random.randint(0, height-1)
            while map[randomY][randomX] == 'x':
                randomX = random.randint(0, width-1)
                randomY = random.randint(0, height-1)
            map[randomY][randomX] = i
            if random.random() < 2 / math.log(width + height):
                break

    # add some rooms
    for i in xrange(1, int(math.floor((width + height) / 8))):
        randomX = random.randint(0, width-1)
        randomY = random.randint(0, height-1)
        randomXRadius = random.randint(1, int(math.sqrt((width-1) / 2)))
        randomYRadius = random.randint(1, int(math.sqrt((height-1) / 2)))
        randomXStart = max(0, min(width-1, randomX - randomXRadius - 1))
        randomXStop = max(0, min(width-1, randomX + randomXRadius))
        randomYStart = max(0, min(height-1, randomY - randomYRadius - 1))
        randomYStop = max(0, min(height-1, randomY + randomYRadius))
        for x in xrange(randomXStart, randomXStop + 1):
            for y in xrange(randomYStart, randomYStop + 1):
                map[y][x] = 'o'

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
for y in map:
    print ''.join(y)
print str(startX) + " " + str(startY)
print str(endX) + " " + str(endY)
