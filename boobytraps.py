# TODO create type for positions, map?
# TODO rethink function names, class needed?

import fileinput


class BoobyTraps:
    def __init__(self, input):
        self.dominationOrder = input[0]

        #self.mapWidth = int(input[1][0])
        self.mapHeight = int(input[1][2])

        self.map = input[2:self.mapHeight+2]

        self.startX = int(input[self.mapHeight+2][0])
        self.startY = int(input[self.mapHeight+2][2])

        self.endX = int(input[self.mapHeight+3][0])
        self.endY = int(input[self.mapHeight+3][2])

    #TODO return map with all smaller traps set to o
    def updateMap(self, map, trapTriggered):
        pass

    #TODO get adjacient fields that aren't walls
    def getAdjacient(self, map, x, y):
        pass

    #TODO implement
    def getMinMoves(self, map, start, end):
        #for adj in self.getAdjacient(map, start[0], start[1]):
        #    pass
        return 17

    def raidtomb(self):
        map = self.map
        start = [self.startX, self.startY]
        end = [self.endX, self.endY]
        return self.getMinMoves(map, start, end)


def main():
    # get input without line terminators
    input = []
    for line in fileinput.input():
        input.append(line.strip())

    # create BoobyTraps object from input
    boobytraps = BoobyTraps(input)

    # compute and output minimum number of moves needed to reach the end
    # position from the start position
    minMoves = boobytraps.raidtomb()
    print minMoves

if __name__ == "__main__":
    main()
