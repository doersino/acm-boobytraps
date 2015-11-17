#TODO maybe cell class with coords and value, change map accordingly
#TODO getAt, setAt neccessary, especially in the map class itself?
#TODO """-style function comments
#TODO maybe identify coords by integer, like width*y+x
#TODO print IMPOSSIBLE if impossible
#TODO -v flag? with colorized map + path output after each step

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
        return hash(self.x * self.y)  # TODO maybe not a good hash?

    def __str__(self):
        return 'x: ' + str(self.x) + ', y: ' + str(self.y)


class Map:
    map = None
    width = 0
    height = 0
    trapDominationOrder = None

    # map given as array (rows) of array (fields)
    def __init__(self, width, height, map, trapDominationOrder):
        self.map = map  # TODO deep copy?
        for i, row in enumerate(self.map):
            self.map[i] = list(row)
        self.width = width
        self.height = height

        self.trapDominationOrder = list(trapDominationOrder)

    def __str__(self):  # TODO make prettier, with coord "axes"?, maybe color
        return 'map: ' + str(self.map) + ', trapDominationOrder: ' + str(self.trapDominationOrder)

    # returns a copy of this map
    def clone(self):
        return copy.deepcopy(self)

    # set triggered (<(=?) trapTriggered)) to x
    # for each cell, if in trapDomination order and smaller than traptriggered, set to x
    def updateTraps(self, trapTriggered):
        # get now-triggered traps
        triggeredTraps = []
        for trap in self.trapDominationOrder:
            triggeredTraps.append(trap)
            if trap == trapTriggered:
                break

        for y, row in enumerate(self.map):
            for x, field in enumerate(row):
                if field in triggeredTraps:
                    self.setAt(Coords(x, y), 'x')

    # return array of (max four) adjacent coords that aren't x
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

    def getVisitables(self):
        visitable = []
        for y, row in enumerate(self.map):
            for x, field in enumerate(row):
                if field in ['o'] + self.trapDominationOrder:  # this works because any triggered traps will have been converted to x
                    visitable.append(Coords(x, y))

        return visitable


    def getAt(self, coords):
        return self.map[coords.y][coords.x]

    def setAt(self, coords, char):
        self.map[coords.y][coords.x] = char

    def isTrap(self, char):
        return char in self.trapDominationOrder


# TODO implement, possibly based on http://rebrained.com/?p=392
def raidtomb(map, start, end, visited=[], distances={}, predecessors={}):
    print start
    if not visited:
        distances[start] = 0
    if start == end:
        path = []
        while end != None:
            path.append(end)
            end = predecessors.get(end)
        return distances[start], path[::-1]
    for neighbor in map.getAdjacent(start):
        if neighbor not in visited:
            neighbordist = distances.get(neighbor, sys.maxint)
            tentativedist = distances[start] + 1
            if tentativedist < neighbordist:
                distances[neighbor] = tentativedist
                predecessors[neighbor] = start
    visited.append(start)
    if map.isTrap(map.getAt(start)):
        map.updateTraps(map.getAt(start))
    unvisiteds = dict((k, distances.get(k,sys.maxint)) for k in map.getVisitables() if k not in visited)
    raided = False
    while unvisiteds:
        closestnode = min(unvisiteds, key=unvisiteds.get)
        try:
            raided = raidtomb(map,closestnode,end,visited,distances,predecessors)
            break
        except KeyError, e:
            del unvisiteds[closestnode]
        except:
            raise

    return raided or "IMPOSSIBLE"
    #else backtrack

# TODO implement, possibly based on http://rebrained.com/?p=392
def raidtomb_buggy(map, start, end, visited=[], distances={}, predecessors={}):
    print start
    if not visited:
        distances[start] = 0
    if start == end:
        path = []
        while end != None:
            path.append(end)
            end = predecessors.get(end)
        return distances[start], path[::-1]
    for neighbor in map.getAdjacent(start):
        if neighbor not in visited:
            neighbordist = distances.get(neighbor, sys.maxint)
            tentativedist = distances[start] + 1
            if tentativedist < neighbordist:
                distances[neighbor] = tentativedist
                predecessors[neighbor] = start
    visited.append(start)
    if map.isTrap(map.getAt(start)):
        map.updateTraps(map.getAt(start))
    unvisiteds = dict((k, distances.get(k,sys.maxint)) for k in map.getVisitables() if k not in visited)
    closestnode = min(unvisiteds, key=unvisiteds.get)
    return raidtomb_buggy(map,closestnode,end,visited,distances,predecessors)


def main():
    # get input without line terminators
    input = []
    for line in fileinput.input():
        input.append(line.strip())

    # parse input
    trapDominationOrder = input[0]
    mapWidth = int(input[1][0])
    mapHeight = int(input[1][2])
    map = Map(mapWidth, mapHeight, input[2:mapHeight+2], trapDominationOrder)

    startX = int(input[mapHeight+2][0])
    startY = int(input[mapHeight+2][2])
    start = Coords(startX, startY)

    endX = int(input[mapHeight+3][0])
    endY = int(input[mapHeight+3][2])
    end = Coords(endX, endY)

    # compute and output minimum number of moves needed to reach the end
    # position from the start position
    print raidtomb(map, start, end)
    #print map

    # test getAdjacent
    #print map.getAt(Coords(3, 5))
    #for i in map.getAdjacent(Coords(3, 5)):
    #    print i
    #    print map.getAt(i)
    #print map.getAt(Coords(1, 2))

    #print map
    #if map.isTrap('o'):
    #    map.updateTraps('o')
    #print map

if __name__ == "__main__":
    main()
