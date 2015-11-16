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
    trapDominationOrder = None

    # map given as array (rows) of array (fields)
    def __init__(self, map, trapDominationOrder):
        self.map = map
        for i, row in enumerate(map):
            map[i] = list(row)

        self.trapDominationOrder = list(trapDominationOrder)

    def __str__(self):
        return 'map: ' + str(self.map) + ', trapDominationOrder: ' + str(self.trapDominationOrder)

    # returns a copy of this map
    def clone(self):
        return copy.deepcopy(self)

    #TODO set triggered (<(=?) trapTriggered)) to o
    def updateTraps(self, trapTriggered):
        # for each cell, if in trapDomination order and smaller than traptriggered, set to o
        pass

    # TODO implement
    def getAdjacient(self, coords):
        # return array of (max four) adjacient coords
        pass

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

if __name__ == "__main__":
    main()
