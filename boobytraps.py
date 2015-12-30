#!/usr/bin/python2.7

import fileinput
import copy
import sys
import Queue


class Cell:
    """Cell with x and y coordinates and value."""

    x = 0
    y = 0
    value = 'x'

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.value == other.value

    def __hash__(self):
        return hash(self.x * self.y * self.value)

    def __str__(self):
        return 'x: ' + str(self.x) + ', y: ' + str(self.y) + ', value: ' + str(self.value)


class Traps:
    """Traps and their domaination order."""

    trapDominationOrder = None
    trapDominationLookup = None

    def __init__(self, trapDominationOrder):
        self.trapDominationOrder = list(trapDominationOrder)
        self.trapDominationLookup = {}
        for i in enumerate(self.trapDominationOrder):
            self.trapDominationLookup[i[1]] = i[0] + 1  # 0 is reserved for empty cells in the path finder

    def __str__(self):
        return 'trapDominationOrder: ' + str(self.trapDominationOrder) + ', trapDominationLookup: ' + str(self.trapDominationLookup)

    def getIndex(self, char):
        """Get the index of a trap."""
        return self.trapDominationLookup[char]

    def isTrap(self, char):
        """Check if a cell value is a trap."""
        return char in self.trapDominationOrder


class Map:
    """Map 2D array, along with width, height and the trap domination order."""

    map = None
    traps = None
    width = 0
    height = 0

    # map must be given as string array (rows) of string arrays (fields)
    def __init__(self, width, height, map, traps):
        self.width = width
        self.height = height

        self.map = copy.deepcopy(map)
        for i, row in enumerate(self.map):
            self.map[i] = list(row)
        self.traps = traps

    def __str__(self):
        return 'map: ' + str(self.map) + ', traps: ' + str(self.traps)

    def prettyprint(self, start, end, path=[]):
        """Print the map with coordinate axes and different colors for different
        cell types.
        """
        xLabel = "  0123->x"
        yLabel = "0123|vy"

        # print x-axis label
        print xLabel

        for y, row in enumerate(self.map):
            # print y-axis label
            if y < len(yLabel):
                sys.stdout.write(yLabel[y] + " ")
            else:
                sys.stdout.write("  ")

            for x, field in enumerate(row):
                prefix = ""
                suffix = "\033[0m"

                # highlight empty fields
                if field == 'o':
                    prefix = prefix + "\033[37m"  # light gray

                # highlight path depending on completeness
                if Cell(x, y, self.getAt(x, y)) in path:
                    if end in path:
                        prefix = prefix + "\033[42m"  # green background
                    else:
                        prefix = prefix + "\033[47m\033[90m"  # dark gray text on light gray background

                # highlight traps
                if self.traps.isTrap(field):
                    prefix = prefix + "\033[31m"  # red

                # highlight start and end
                if Cell(x, y, self.getAt(x, y)) == start:
                    prefix = prefix + "\033[1m\033[44m"  # bold on blue background
                if Cell(x, y, self.getAt(x, y)) == end:
                    prefix = prefix + "\033[1m\033[4m\033[41m"  # bold underlined on red background

                # highlight end differently if it is a trap to maintain readability
                if Cell(x, y, self.getAt(x, y)) == end and self.traps.isTrap(field):
                    prefix = prefix + "\033[1m\033[4m\033[45m"  # pink background

                sys.stdout.write(prefix + field + suffix)
            print

    def getAdjacent(self, cell):
        """Get the (up to four) cells adjacent to a cell."""
        adj = []

        # left neighbor
        if cell.x > 0:
            candidate = Cell(cell.x - 1, cell.y, self.map[cell.y][cell.x - 1])
            if candidate.value != 'x':
                adj.append(candidate)

        # right neighbor
        if cell.x < self.width - 1:
            candidate = Cell(cell.x + 1, cell.y, self.map[cell.y][cell.x + 1])
            if candidate.value != 'x':
                adj.append(candidate)

        # top neighbor
        if cell.y > 0:
            candidate = Cell(cell.x, cell.y - 1, self.map[cell.y - 1][cell.x])
            if candidate.value != 'x':
                adj.append(candidate)

        # bottom neighbor
        if cell.y < self.height - 1:
            candidate = Cell(cell.x, cell.y + 1, self.map[cell.y + 1][cell.x])
            if candidate.value != 'x':
                adj.append(candidate)

        return adj

    def getAt(self, x, y):
        """Get the cell value at position x, y."""
        return self.map[y][x]


class Graph:
    """Graph represented as an adjacency list."""

    graph = None

    def __init__(self, map):
        self.graph = {}
        for y, row in enumerate(map.map):
            for x, field in enumerate(row):
                if field != 'x':  # ignore wall cells: irrelevant for path finding
                    cell = Cell(x, y, field)
                    self.graph[cell] = map.getAdjacent(cell)

    def __str__(self):
        return 'graph: ' + str(self.graph)

    def prettyprint(self):
        """Print the graph in a readable way."""
        for field in self.graph:
            print str(field)
            for adj in self.graph[field]:
                if adj.x < field.x:
                    arrow = u'\u25c0'  # right
                elif adj.x > field.x:
                    arrow = u'\u25b6'  # left
                elif adj.y < field.y:
                    arrow = u'\u25b2'  # up
                else:
                    arrow = u'\u25bc'  # down
                print "\t" + arrow + " " + str(adj)


def raidtomb(graph, traps, start, end):
    """Find the shortest path between start and end cells ("raid the tomb")
    using breadth-first search, returning the number of moves and the path.
    """
    graph = graph.graph
    q = Queue.Queue()

    # initialize visited structure
    visited = {}
    visited[0] = set()
    for i in traps.trapDominationLookup.values():
        visited[i] = set()

    # add start to queue
    if traps.isTrap(start.value):
        c = {'cell': start, 'path': [start], 'triggered': traps.getIndex(start.value)}
        visited[c['triggered']].add(c['cell'])
    else:
        c = {'cell': start, 'path': [start], 'triggered': 0}
        visited[0].add(c['cell'])
    q.put(c)

    while not q.empty():
        # get new cell
        c = q.get()

        # add all neighbors of c to queue
        for neighbor in graph[c['cell']]:
            if neighbor not in c['path'] and neighbor not in visited[c['triggered']]:

                # neigbor is trap cell
                if traps.isTrap(neighbor.value):
                    v = neighbor.value
                    if traps.getIndex(v) > c['triggered']:
                        n = {'cell': neighbor, 'path': c['path'] + [neighbor], 'triggered': traps.getIndex(v)}
                        if neighbor == end:
                            return len(n['path']) - 1, n['path']
                        else:
                            q.put(n)
                            visited[n['triggered']].add(neighbor)

                # neigbor is empty cell
                else:
                    n = {'cell': neighbor, 'path': c['path'] + [neighbor], 'triggered': c['triggered']}
                    if neighbor == end:
                        return (len(n['path']) - 1, n['path'])
                    else:
                        q.put(n)
                        visited[n['triggered']].add(neighbor)

    return -1, c['path']


def main():
    # process verbose option
    verbose = len(sys.argv) > 1 and sys.argv[1] == "-v"
    if verbose:
        del sys.argv[1]

    # get input without line breaks
    input = []
    for line in fileinput.input():
        input.append(line.strip())

    # parse input
    traps = Traps(input[0])

    mapWidth, mapHeight = [int(i) for i in input[1].split(" ")]
    map = Map(mapWidth, mapHeight, input[2:mapHeight+2], traps)

    graph = Graph(map)

    startX, startY = [int(i) for i in input[mapHeight+2].split(" ")]
    startValue = map.getAt(startX, startY)
    start = Cell(startX, startY, startValue)

    endX, endY = [int(i) for i in input[mapHeight+3].split(" ")]
    endValue = map.getAt(endX, endY)
    end = Cell(endX, endY, endValue)

    # raid the tomb
    moves, path = raidtomb(graph, traps, start, end)

    # output result
    if verbose:
        print "Map:"
        map.prettyprint(start, end, path)
        print "Minimum number of moves to reach the end position from the start position:"
    if moves >= 0:
        print moves
    else:
        print "IMPOSSIBLE"
        sys.exit(1)

if __name__ == "__main__":
    main()
