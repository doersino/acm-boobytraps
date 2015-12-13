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
parser.add_argument("--start", metavar="STARTX,STARTY", help="comma-separated coordinates (x,y) of the start postion, must be smaller than WIDTH,HEIGHT (default: random)")
parser.add_argument("--end", metavar="ENDX,ENDY", help="comma-separated coordinates (x,y) of the end postion, must be smaller than WIDTH,HEIGHT (default: random)")
parser.add_argument("--mode", choices=["random", "dungeon"], help="random (default) or dungeon (with corridors and rooms)")
parser.add_argument("--complexity", type=float, help="complexity of the generated map, in terms of wall cell/empty cell ratio and trap frequency, must be a positive float with larger numbers meaning higher complexity (default: 1)")
parser.add_argument("--seed", help="seed for random number generator used during map generation")
parser.add_argument("--printseed", dest="printseed", action="store_true", help="print the seed to stderr after printing the map (might come in handy when no seed is specified using the --seed option)")
parser.add_argument("--no-printseed", dest="printseed", action="store_false", help="don't print the seed to stderr after printing the map (default)")
parser.set_defaults(printseed=False)
args = parser.parse_args()

if args.width * args.height > 40000:
    sys.exit("usage: see " + __file__ + " -h\n" + __file__ + ": error: WIDTH * HEIGHT must not exceed 40000")

if args.start:
    startX, startY = [int(i) for i in args.start.split(",")]
    if startX > args.width:
        sys.exit("usage: see " + __file__ + " -h\n" + __file__ + ": error: STARTX must be smaller than WIDTH")
    if startY > args.height:
        sys.exit("usage: see " + __file__ + " -h\n" + __file__ + ": error: STARTY must be smaller than HEIGHT")
else:
    startX = startY = False

if args.end:
    endX, endY = [int(i) for i in args.end.split(",")]
    if endX > args.width:
        sys.exit("usage: see " + __file__ + " -h\n" + __file__ + ": error: ENDX must be smaller than WIDTH")
    if endY > args.height:
        sys.exit("usage: see " + __file__ + " -h\n" + __file__ + ": error: ENDY must be smaller than HEIGHT")
else:
    endX = endY = False

if not args.mode:
    args.mode = "random"

if not args.complexity:
    args.complexity = 10.0
elif args.complexity <= 0:
    sys.exit("usage: see " + __file__ + " -h\n" + __file__ + ": error: COMPLEXITY must be a positive float")

if not args.seed:
    rand = random.SystemRandom()
    args.seed = str(rand.randint(0, sys.maxint))

# set complexity
complexity = args.complexity

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
    for i in xrange(1, int(width * height * 1.5 * (10/complexity))):
        randomX = random.randint(0, width-1)
        randomY = random.randint(0, height-1)
        map[randomY][randomX] = 'o'

    # add some traps
    for i in trapDominationOrdering[::-1]:
        randomX = random.randint(0, width-1)
        randomY = random.randint(0, height-1)
        map[randomY][randomX] = i
        if random.random() < 1 / math.sqrt(width * height * (complexity/10)):
            break

    # set start and end points
    if startX is False:
        startX = random.randint(0, width-1)
        startY = random.randint(0, height-1)
        tries = 0
        while map[startY][startX] == 'x' and tries < 42:
            startX = random.randint(0, width-1)
            startY = random.randint(0, height-1)
            tries += 1
    if endX is False:
        endX = random.randint(0, width-1)
        endY = random.randint(0, height-1)
        tries = 0
        while (endX == startX and endY == startY) or (map[endY][endX] == 'x' and tries < 42):
            endX = random.randint(0, width-1)
            endY = random.randint(0, height-1)
            tries += 1

    # make sure that start and end aren't walls
    if map[startY][startX] == 'x':
        map[startY][startX] = 'o'
    if map[endY][endX] == 'x':
        map[endY][endX] = 'o'

# dungeon map generation algorithm
elif mode == "dungeon":
    # add some corridors
    # horizontal
    for i in xrange(1, int(math.floor(((width+height) * (10/complexity)) / 4))):
        randomX = random.randint(0, width-1)
        randomY = random.randint(0, height-1)
        randomRadius = random.randint(1, max(1, math.floor((width-1) / 2)))
        randomXStart = max(0, min(width-1, randomX - randomRadius - 1))
        randomXStop = max(0, min(width-1, randomX + randomRadius))
        for x in xrange(randomXStart, randomXStop + 1):
            map[randomY][x] = 'o'

    # vertical
    for i in xrange(1, int(math.floor(((width + height) * (10/complexity)) / 4))):
        randomX = random.randint(0, width-1)
        randomY = random.randint(0, height-1)
        randomRadius = random.randint(1, max(1, math.floor((height-1) / 2)))
        randomYStart = max(0, min(height-1, randomY - randomRadius - 1))
        randomYStop = max(0, min(height-1, randomY + randomRadius))
        for y in xrange(randomYStart, randomYStop + 1):
            map[y][randomX] = 'o'

    # add some random empty cells
    for i in xrange(1, int(math.floor((width+height) * (10/complexity)))):
        randomX = random.randint(0, width-1)
        randomY = random.randint(0, height-1)
        map[randomY][randomX] = 'o'

    # add some traps: no traps wanted in rooms on small maps
    for i in trapDominationOrdering[::-1]:
        while random.random() < .5 * (complexity/10):
            randomX = random.randint(0, width-1)
            randomY = random.randint(0, height-1)
            tries = 0
            while map[randomY][randomX] == 'x' and tries < 42:
                randomX = random.randint(0, width-1)
                randomY = random.randint(0, height-1)
                tries += 1
            if tries < 42:
                map[randomY][randomX] = i
            if random.random() < 2 / math.log((width+height) * (complexity/10)):
                break

    # add some rooms
    for i in xrange(1, int(math.floor(((width + height) * (10/complexity)) / 8))):
        randomX = random.randint(0, width-1)
        randomY = random.randint(0, height-1)
        randomXRadius = random.randint(1, max(1, int(math.sqrt((width-1) / 2))))
        randomYRadius = random.randint(1, max(1, int(math.sqrt((height-1) / 2))))
        randomXStart = max(0, min(width-1, randomX - randomXRadius - 1))
        randomXStop = max(0, min(width-1, randomX + randomXRadius))
        randomYStart = max(0, min(height-1, randomY - randomYRadius - 1))
        randomYStop = max(0, min(height-1, randomY + randomYRadius))
        for x in xrange(randomXStart, randomXStop + 1):
            for y in xrange(randomYStart, randomYStop + 1):
                map[y][x] = 'o'

    # add more traps on giant maps
    if width * height >= 5000:
        for i in trapDominationOrdering[::-1]:
            while random.random() < .67 * (complexity/10):
                randomX = random.randint(0, width-1)
                randomY = random.randint(0, height-1)
                tries = 0
                while map[randomY][randomX] == 'x' and tries < 42:
                    randomX = random.randint(0, width-1)
                    randomY = random.randint(0, height-1)
                    tries += 1
                if tries < 42:
                    map[randomY][randomX] = i
                if random.random() < 1 / math.log((width*height) * (complexity/10)):
                    break

    # set start and end points
    if startX is False:
        startX = random.randint(0, width-1)
        startY = random.randint(0, height-1)
        tries = 0
        while map[startY][startX] == 'x' and tries < 42:
            startX = random.randint(0, width-1)
            startY = random.randint(0, height-1)
            tries += 1
    if endX is False:
        endX = random.randint(0, width-1)
        endY = random.randint(0, height-1)
        tries = 0
        while (endX == startX and endY == startY) or (map[endY][endX] == 'x' and tries < 42):
            endX = random.randint(0, width-1)
            endY = random.randint(0, height-1)
            tries += 1

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

# print seed
if args.printseed:
    sys.stderr.write("Seed: " + str(seed) + "\n")
