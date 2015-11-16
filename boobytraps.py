#TODO maybe cell class with coords and value, change map accordingly

import fileinput
import copy


class Coords:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'x: ' + str(self.x) + ', y: ' + str(self.y)


class Map:
    map = None
    width = 0
    height = 0
    trapDominationOrder = None

    # map given as array (rows) of array (fields)
    def __init__(self, map, trapDominationOrder):
        self.map = map
        for i, row in enumerate(map):
            self.map[i] = list(row)
        self.width = len(self.map[0])
        self.height = len(self.map)

        self.trapDominationOrder = list(trapDominationOrder)

    def __str__(self):
        return 'map: ' + str(self.map) + ', trapDominationOrder: ' + str(self.trapDominationOrder)

    # returns a copy of this map
    def clone(self):
        return copy.deepcopy(self)

    #TODO set triggered (<(=?) trapTriggered)) to x
    def updateTraps(self, trapTriggered):
        # for each cell, if in trapDomination order and smaller than traptriggered, set to o
        pass

    # return array of (max four) adjacient coords that aren't x
    def getAdjacient(self, coords):
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


# TODO implement
def raidtomb(map, start, end):
    return 17


def main():
    # get input without line terminators
    input = []
    for line in fileinput.input():
        input.append(line.strip())

    # parse input
    trapDominationOrder = input[0]
    #mapWidth = int(input[1][0])
    mapHeight = int(input[1][2])
    map = Map(input[2:mapHeight+2], trapDominationOrder)

    startX = int(input[mapHeight+2][0])
    startY = int(input[mapHeight+2][2])
    start = Coords(startX, startY)

    endX = int(input[mapHeight+3][0])
    endY = int(input[mapHeight+3][2])
    end = Coords(endX, endY)

    # compute and output minimum number of moves needed to reach the end
    # position from the start position
    print raidtomb(map, start, end)

    # test getAdjacient
    #for i in map.getAdjacient(Coords(3, 3)):
    #    print i

if __name__ == "__main__":
    main()
