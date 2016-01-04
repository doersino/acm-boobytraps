#!/usr/bin/python2.7

# Finds the shortest path in a map instance adhering to the rules defined in
# boobytraps.pdf. Outputs the length of the path, as well as (optionally) a
# visualization of the path in the map.
#
# Usage: Either of the following three options will work:
#
#        ./boobytraps.py [-v | -v1 | -v2] INPUT_FILE
#        cat INPUT_FILE | ./boobytraps.py [-v | -v1 | -v2]
#        ./gravedivver.py WIDTH HEIGHT | ./boobytraps.py [-v | -v1 | -v2]
#
#        -v  enables output of the map and highlighted path.
#        -v1 is equivalent to -v.
#        -v2 additionally highlights visited fields and, if no path from start
#            to end is found, the "best effort" path.

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
            self.trapDominationLookup[i[1]] = i[0] + 1  # in the path finder, 0 is reserved for empty cells

    def __str__(self):
        return 'trapDominationOrder: ' + str(self.trapDominationOrder) + ', trapDominationLookup: ' + str(self.trapDominationLookup)

    def getIndex(self, char):
        """Get the index (starting with 1) of a trap."""
        return self.trapDominationLookup[char]

    def isTrap(self, char):
        """Check if a cell value is a trap."""
        return char in self.trapDominationOrder


class Map:
    """Map as a 2D char array, along with width, height and the trap domination
    order.
    """

    map = None
    traps = None
    width = 0
    height = 0

    def __init__(self, width, height, map, traps):
        self.width = width
        self.height = height

        # the map should be given as an array (rows) of strings (fields) so we
        # can convert it to a 2D char array here
        self.map = copy.deepcopy(map)
        for i, row in enumerate(self.map):
            self.map[i] = list(row)

        self.traps = traps

    def __str__(self):
        return 'map: ' + str(self.map) + ', traps: ' + str(self.traps)

    def prettyprint(self, start, end, path=[], visited=[]):
        """Print the map with coordinate axes and different colors for different
        cell types. Highlight start, end, a path in the map as well as visited
        cells.
        """
        xLabel = "  0123->x"
        yLabel = "0123|vy"

        # print x-axis label
        print xLabel

        # print row
        for y, row in enumerate(self.map):
            # print y-axis label
            if y < len(yLabel):
                sys.stdout.write(yLabel[y] + " ")
            else:
                sys.stdout.write("  ")

            # print all fields in the current row
            for x, field in enumerate(row):
                prefix = ""
                suffix = "\033[0m"

                # highlight empty fields
                if field == 'o':
                    prefix = prefix + "\033[37m"  # light gray

                # highlight visited fields
                if Cell(x, y, self.getAt(x, y)) in visited:
                    prefix = prefix + "\033[48;5;255m"  # very light gray background

                # highlight path depending on completeness
                if Cell(x, y, self.getAt(x, y)) in path:
                    if end in path:
                        prefix = prefix + "\033[42m"  # green background
                    else:
                        prefix = prefix + "\033[90m\033[47m"  # dark gray text on light gray background

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
                    prefix = prefix + "\033[45m"  # pink background

                sys.stdout.write(prefix + field + suffix)
            print

    def printLatexDrawCommands(self, start, end, path=[]):
        """Quick-and-dirty way of printing the draw commands for a LaTex
        representation of the map (using tikz).
        In the output of this function, adjust the scale factor by modifying the
        argument of \BTmap if necessary, or change \BTpath to \BTpathX if you
        want to highlight an incorrect path.
        The following macros need to be defined in the preamble:

        \def\BTwallcolor{gray}
        \def\BTtrapcolor{red}
        \def\BTpathXcolor{red!60!black}
        \def\BTpathcolor{green!60!black}
        \def\BTstartcolor{blue!85!black}
        \def\BTendcolor{red!75!black}

        \newcommand{\BTmap}[2]{ % scale factor & draw commands
            \begin{center}
                \begin{tikzpicture}[scale=#1,every node/.style={transform shape}]
                    #2
                \end{tikzpicture}
            \end{center}
        }
        \newcommand{\BTwall}[2]{ % bottom left corner & top right corner
            \fill[\BTwallcolor] (#1) rectangle (#2);
        }
        \newcommand{\BTtrap}[2]{ % position & letter
            \node at (#1) {\LARGE\bfseries\color{\BTtrapcolor} #2};
        }
        \newcommand{\BTpathX}[1]{ % path
            \draw[\BTpathXcolor, dotted, thick] #1;
        }
        \newcommand{\BTpath}[1]{ % path
            \draw[\BTpathcolor, solid, very thick] #1;
        }
        \newcommand{\BTstart}[1]{ % position
            \path[fill=\BTstartcolor] (#1) circle (0.25);
        }
        \newcommand{\BTend}[1]{ % position
            \path[fill=\BTendcolor] (#1) circle (0.25);
        }
        \newcommand{\BTgrid}[1]{ % height,width
            \draw[step=1,black,thick] (0,0) grid (#1);
        }
        """

        print '\BTmap{1}{'

        # draw walls
        for y, row in enumerate(self.map):
            for x, field in enumerate(row):
                if field == 'x':
                    print '\BTwall{' + str(x) + ',' + str(self.height-y) + '}{' + str(x+1) + ',' + str(self.height-(y+1)) + '}'

        # draw traps
        for y, row in enumerate(self.map):
            for x, field in enumerate(row):
                if self.traps.isTrap(field):
                    print '\BTtrap{' + str(x) + '.5,' + str(self.height-(y+1)) + '.5}{' + field + '}'

        # draw path
        sys.stdout.write('\BTpath{')
        for i, cell in enumerate(path):
            if i != 0:
                sys.stdout.write(' -- ')
            sys.stdout.write('(' + str(cell.x) + '.5,' + str(self.height-(cell.y+1)) + '.5)')
        print '}'

        # draw start
        for y, row in enumerate(self.map):
            for x, field in enumerate(row):
                if Cell(x, y, self.getAt(x, y)) == start:
                    print '\BTstart{' + str(x) + '.5,' + str(self.height-(y+1)) + '.5}'

        # draw end
        for y, row in enumerate(self.map):
            for x, field in enumerate(row):
                if Cell(x, y, self.getAt(x, y)) == end:
                    print '\BTend{' + str(x) + '.5,' + str(self.height-(y+1)) + '.5}'

        # draw grid
        print '\BTgrid{' + str(self.width) + ',' + str(self.height) + '}'

        print '}'

    def getAdjacent(self, cell):
        """Get the (up to four) cells adjacent to a given cell."""
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

        # add eligible neighbors to queue and check if one of them is the end
        for neighbor in graph[c['cell']]:
            if neighbor not in visited[c['triggered']]:

                # make sure the neigbor can be visited and update maximum triggered trap
                triggered = c['triggered']
                if traps.isTrap(neighbor.value):
                    v = neighbor.value
                    if traps.getIndex(v) <= c['triggered']:  # trap already in path
                        continue
                    triggered = traps.getIndex(v)

                # create new queue frame
                n = {'cell': neighbor, 'path': c['path'] + [neighbor], 'triggered': triggered}

                # check if the end has been reached
                if neighbor == end:
                    return len(n['path']) - 1, n['path'], set().union(*visited.values())
                else:
                    q.put(n)
                    visited[n['triggered']].add(neighbor)

    # return longest/"best effort" path
    return -1, c['path'], set().union(*visited.values())


def main():
    # process verbose options
    verbose = len(sys.argv) > 1 and sys.argv[1] in ["-v", "-v1", "-v2"]
    verbose2 = verbose and sys.argv[1] == "-v2"
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
    moves, path, visited = raidtomb(graph, traps, start, end)

    # print LaTex draw commands for the map
    #map.printLatexDrawCommands(start, end, path)
    #sys.exit()

    # discard visited and "best effort" path if the verbose2 option is disabled
    if not verbose2:
        if moves < 0:  # no path found
            path = []
        visited = []

    # output result
    if verbose:
        print "Map:"
        map.prettyprint(start, end, path, visited)
        print "Minimum number of moves to reach the end position from the start position:"
    if moves >= 0:
        print moves
    else:
        print "IMPOSSIBLE"
        sys.exit(1)

if __name__ == "__main__":
    main()
