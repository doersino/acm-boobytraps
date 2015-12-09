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


class Map:
    """Map with width, height and the trap domination order."""

    map = None
    trapDominationOrder = None
    width = 0
    height = 0

    # map must be given as string array (rows) of string arrays (fields)
    def __init__(self, width, height, map, trapDominationOrder):
        self.width = width
        self.height = height

        self.map = copy.deepcopy(map)
        for i, row in enumerate(self.map):
            self.map[i] = list(row)
        self.trapDominationOrder = list(trapDominationOrder)

    def __str__(self):
        return 'map: ' + str(self.map) + ', trapDominationOrder: ' + str(self.trapDominationOrder)

    def prettyprint(self, start, end, path=[]):
        """Print the map with coordinate axes and different colors for different cell types."""
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

                # highlight traps
                if field in self.trapDominationOrder:
                    prefix = prefix + "\033[31m"  # red

                # highlight empty fields
                if field == 'o':
                    prefix = prefix + "\033[37m"  # light gray

                # highlight start and end
                if Cell(x, y, self.getAt(x, y)) == start:
                    prefix = prefix + "\033[1m\033[90m"  # bold dark gray
                if Cell(x, y, self.getAt(x, y)) == end:
                    prefix = prefix + "\033[1m\033[4m\033[90m"  # bold underlined dark gray

                # highlight path
                if Cell(x, y, self.getAt(x, y)) in path:
                    prefix = prefix + "\033[42m"  # green background

                sys.stdout.write(prefix + field + suffix)
            print

    def getAdjacent(self, cell):
        """Get the (up to four) adjacent cells."""
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

    def setAt(self, cell):
        """Set the cell value."""
        self.map[cell.y][cell.x] = cell.value

    def isTrap(self, char):
        """Check if a cell value is a trap."""
        return char in self.trapDominationOrder


class Graph:
    """Graph represented as an adjacency list."""

    map = None
    graph = None

    def __init__(self, map):
        self.map = map

        self.graph = {}
        for y, row in enumerate(map.map):
            for x, field in enumerate(row):
                # ignore wall cells: irrelevant for path finding
                if field != 'x':
                    cell = Cell(x, y, field)
                    adj = map.getAdjacent(cell)
                    adjDict = {}
                    for i in adj:
                        adjDict[i] = 1
                    self.graph[cell] = adjDict

        self.optimize()

    def __str__(self):
        return 'map: ' + str(self.map) + ', graph: ' + str(self.graph)

    def prettyprint(self):
        """Print the graph in a readable way."""
        for field in self.graph:
            sys.stdout.write("'" + str(field) + "': {")
            for adj in self.graph[field]:
                sys.stdout.write("'" + str(adj) + "': " + str(self.graph[field][adj]) + ",")
            sys.stdout.write("}")
            print

    def optimize(self):
        """Reduce size and complexity of graph by removing deadends and collapsing adjacent cells with no branches to other cells."""
        # do all this recursively until no change?
        # if two neigbours and in line with no other neighbors, concat
        # if only one neighbor and both not traps, concat
        #for field in self.graph:
        #    if len(self.graph[field]) == 1:
        #        self.graph[field] = self.graph[field][self.graph[field].keys()[0]]
        #        del self.graph[self.graph[field][self.graph[field].keys()[0]]]
        # remove deadends (if != start, end)
        # ---
        #for field in list(self.graph):
        #    try:
        #        if len(self.graph[field]) == 1 and field.value == 'o':
        #            for i in self.graph[field]:
        #                child = i
        #            if child.value == 'o':
        #                print field
        #                print self.graph[field].keys()[0]
        #                self.graph[field] = self.graph[child]
        #                del self.graph[child]
        #    except KeyError:
        #        pass
        pass

    def update(self, triggeredTrapCell):
        # compute list of triggered traps
        triggeredTraps = []
        for trap in self.map.trapDominationOrder:
            triggeredTraps.append(trap)
            if trap == triggeredTrapCell.value:
                break

        # remove all referecences to triggered traps from the graph
        for cell in list(self.graph):
            if cell.value in triggeredTraps:
                del self.graph[cell]
                for cell2 in self.graph:
                    if cell in self.graph[cell2]:
                        del self.graph[cell2][cell]

        self.optimize()


def raidtombBacktracking(graph, start, end):
    """Find the shortest path between start and end cells ("raid the tomb") using backtracking"""
    trapDominationOrder = graph.map.trapDominationOrder
    trapDominationLookup = {}
    for i in enumerate(trapDominationOrder):
        trapDominationLookup[i[1]] = i[0]
    print trapDominationLookup

    graph = graph.graph
    q = Queue.Queue()

    start = {'cell': start, 'path': [start], 'triggered': False}
    q.put(start)

    c = start
    while c['cell'] != end and not q.empty():
        # add all neighbors of c to queue
        for neighbor in graph[c['cell']].keys():
            if neighbor not in c['path']:  # TODO and not < max triggered trap
                if neighbor.value != 'o':
                    v = neighbor.value
                    if trapDominationLookup[v] > c['triggered']:
                        n = {'cell': neighbor, 'path': c['path'] + [neighbor], 'triggered': trapDominationLookup[v]}
                        if neighbor == end:
                            return (len(n['path']), n['path'])
                        else:
                            q.put(n)
                else:
                    n = {'cell': neighbor, 'path': c['path'] + [neighbor], 'triggered': c['triggered']}
                    if neighbor == end:
                        return (len(n['path']), n['path'])
                    else:
                        q.put(n)

        # get new c
        c = q.get()

    return "IMPOSSIBLE"


def raidtomb(graph, start, end, visited=[], distances={}, predecessors={}):
    """Find the shortest path between start and end cells ("raid the tomb")"""
    # algorithm based on http://rebrained.com/?p=392

    # detect if it's the first time through, set current distance to zero
    if not visited:
        distances[start] = 0

    if start == end:
        # we've found our end node, now find the path to it, and return
        path = []
        while end is not None:
            path.append(end)
            end = predecessors.get(end)
        return distances[start], path[::-1]

    # process neighbors as per algorithm, keep track of predecessors
    for neighbor in graph.graph[start]:
        if neighbor not in visited:
            neighbordist = distances.get(neighbor, sys.maxint)
            tentativedist = distances[start] + graph.graph[start][neighbor]
            if tentativedist < neighbordist:
                distances[neighbor] = tentativedist
                predecessors[neighbor] = start

    # neighbors processed, now mark the current node as visited
    visited.append(start)

    # trigger traps
    if start.value != 'o':
        graph = copy.deepcopy(graph)
        graph.update(start)

    # find the closest reachable unvisited node to the start
    unvisiteds = dict((k, distances.get(k, sys.maxint)) for k in graph.graph if k not in visited and distances.get(k, sys.maxint) < sys.maxint)
    if not unvisiteds:
        return "IMPOSSIBLE"
    closestnode = min(unvisiteds, key=unvisiteds.get)

    while unvisiteds.pop(closestnode, False):
        # now we can take the closest node and recurse, making it current
        raided = raidtomb(graph, closestnode, end, copy.deepcopy(visited), copy.deepcopy(distances), predecessors)

        # return to recursive call before most recent trap cell (i.e. recursive call with trap cell as closestnode)
        if raided == "IMPOSSIBLE" and closestnode.value != 'o' and unvisiteds:
            # ignore the trap cell and try other adjacent cells
            closestnode = min(unvisiteds, key=unvisiteds.get)
        else:
            # only if that fails and if no previous recursive trap cell call was made, we can be sure that the previous return value is correct
            return raided
    return "IMPOSSIBLE"


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
    startValue = map.getAt(startX, startY)
    start = Cell(startX, startY, startValue)

    endX, endY = [int(i) for i in input[mapHeight+3].split(" ")]
    endValue = map.getAt(endX, endY)
    end = Cell(endX, endY, endValue)

    graph = Graph(map)

    # compute and output minimum number of moves needed to reach the end
    # position from the start position ("raid the tomb")
    #raided = raidtomb(graph, start, end)
    raided = raidtombBacktracking(graph, start, end)

    # print result
    if verbose:
        if raided == "IMPOSSIBLE":
            print "Map:"
            map.prettyprint(start, end)
            print raided
            sys.exit(1)
        else:
            #print "Path:"
            #for i in raided[1]:
            #    print i
            print "Map:"
            map.prettyprint(start, end, raided[1])
            print "Minimum number of moves to reach the end position from the start position:"
            print raided[0]
    else:
        if raided == "IMPOSSIBLE":
            print raided
            sys.exit(1)
        else:
            print raided[0]

if __name__ == "__main__":
    main()
