import fileinput
import copy
import sys


class Coords:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x * self.y)

    def __str__(self):
        return 'x: ' + str(self.x) + ', y: ' + str(self.y)


class Map:
    map = None
    width = 0
    height = 0
    trapDominationOrder = None
    activeTraps = None

    # map given as array (rows) of arrays (fields)
    def __init__(self, width, height, map, trapDominationOrder):
        self.map = copy.deepcopy(map)
        for i, row in enumerate(self.map):
            self.map[i] = list(row)

        self.width = width
        self.height = height

        self.trapDominationOrder = list(trapDominationOrder)
        self.activeTraps = list(trapDominationOrder)

    def __str__(self):
        return 'map: ' + str(self.map) + ', trapDominationOrder: ' + str(self.trapDominationOrder)

    def clone(self):
        return copy.deepcopy(self)

    def updateTraps(self, trapTriggered):
        # get now-triggered traps
        triggeredTraps = []
        for trap in self.trapDominationOrder:
            triggeredTraps.append(trap)
            if trap == trapTriggered:
                break

        # update still-active traps
        self.activeTraps = list(set(self.trapDominationOrder) - set(triggeredTraps))

        # update map
        for y, row in enumerate(self.map):
            for x, field in enumerate(row):
                if field in triggeredTraps:
                    self.setAt(Coords(x, y), 'x')

    def getAdjacent(self, coords):
        adj = []

        # left
        if coords.x > 0:
            candidate = Coords(coords.x - 1, coords.y)
            if self.getAt(candidate) != 'x':
                adj.append(candidate)

        # right
        if coords.x < self.width - 1:
            candidate = Coords(coords.x + 1, coords.y)
            if self.getAt(candidate) != 'x':
                adj.append(candidate)

        # top
        if coords.y > 0:
            candidate = Coords(coords.x, coords.y - 1)
            if self.getAt(candidate) != 'x':
                adj.append(candidate)

        # bottom
        if coords.y < self.height - 1:
            candidate = Coords(coords.x, coords.y + 1)
            if self.getAt(candidate) != 'x':
                adj.append(candidate)

        return adj

    def getAt(self, coords):
        return self.map[coords.y][coords.x]

    def setAt(self, coords, char):
        self.map[coords.y][coords.x] = char

    def isTrap(self, char):
        return char in self.trapDominationOrder


# algorithm based on http://rebrained.com/?p=392
def raidtomb(map, start, end, visited=[], distances={}, predecessors={}):
    #print start
    #print map.activeTraps

    # initialize
    if not visited:
        distances[start] = 0

    # if the end has been reached, return distance and path
    if start == end:
        path = []
        while end is not None:
            path.append(end)
            end = predecessors.get(end)
        return distances[start], path[::-1]

    # process neighbors and mark current cell as visited
    for neighbor in map.getAdjacent(start):
        if neighbor not in visited:
            neighbordist = distances.get(neighbor, sys.maxint)
            tentativedist = distances[start] + 1
            if tentativedist < neighbordist:
                distances[neighbor] = tentativedist
                predecessors[neighbor] = start
    visited.append(start)

    # recurse with closest unvisited cell
    map = map.clone()
    if map.isTrap(map.getAt(start)):
        map.updateTraps(map.getAt(start))
    unvisiteds = dict((k, distances.get(k, sys.maxint)) for k in map.getAdjacent(start) if k not in visited)
    raided = False
    while unvisiteds:
        closestnode = min(unvisiteds, key=unvisiteds.get)
        try:
            raided = raidtomb(map, closestnode, end, copy.deepcopy(visited), copy.deepcopy(distances), predecessors)
            if raided != "IMPOSSIBLE":
                break
            else:
                del unvisiteds[closestnode]
        except KeyError:
            del unvisiteds[closestnode]
        except:
            raise

    return raided or "IMPOSSIBLE"


def main():
    # process verbose option
    verbose = len(sys.argv) > 1 and sys.argv[1] == "-v"
    if verbose:
        del sys.argv[1]

    # get input without line terminators
    input = []
    for line in fileinput.input():
        input.append(line.strip())

    # parse input
    trapDominationOrder = input[0]
    mapWidth, mapHeight = [int(i) for i in input[1].split(" ")]
    map = Map(mapWidth, mapHeight, input[2:mapHeight+2], trapDominationOrder)

    startX, startY = [int(i) for i in input[mapHeight+2].split(" ")]
    start = Coords(startX, startY)

    endX, endY = [int(i) for i in input[mapHeight+3].split(" ")]
    end = Coords(endX, endY)

    # compute and output minimum number of moves needed to reach the end
    # position from the start position ("raid the tomb")
    raided = raidtomb(map, start, end)
    if verbose:
        if raided == "IMPOSSIBLE":
            print raided
        else:
            for i in raided[1]:
                print i
            print raided[0]
    else:
        if raided == "IMPOSSIBLE":
            print raided
        else:
            print raided[0]

if __name__ == "__main__":
    main()
