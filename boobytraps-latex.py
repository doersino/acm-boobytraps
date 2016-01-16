#!/usr/bin/python2.7

# Using boobytraps.py, generates LaTeX code snippets related to boobytraps.py:
# The map subcommand prints the draw commands for a LaTeX representation of the
# map and path (using TikZ).
# The slides subcommand prints the source code of Beamer slides detailing all
# steps of the path finding algorithm.
#
# Usage: Either of the following two options will work:
#
#        cat INPUT_FILE | ./boobytraps-latex.py [map [OPTIONS]] [slides [OPTIONS]]
#        ./gravedigger.py WIDTH HEIGHT | ./boobytraps-latex.py [map [OPTIONS]] [slides [OPTIONS]]
#
#        For OPTIONS, see boobytraps-latex.py -h.

from boobytraps import *


# TODO improve path macro
# TODO update docstring with options, graph drawing
def printLatexMapDrawCommands(map, start, end, graph=False, path=[], maybepaths=[], nopaths=[], highlight=[], scale=1, showCoords=False):
    """Quick-and-dirty way of printing the draw commands for a LaTeX
    representation of the map (using tikz).
    If you want to highlight an incorrect path, change \BTpath to \BTnopath
    in the output of this function, and if you want to highlight a cell, use
    the \BThighlight macro.
    Make sure to \input{boobytraps-latex-preample.tex} in your .tex file.
    """

    print '\BTmap{' + str(scale) + '}{'

    # draw highlights
    for y, row in enumerate(map.map):
        for x, field in enumerate(row):
            if Cell(x, y, map.getAt(x, y)) in highlight:
                print '\BThighlight{' + str(x) + '}{' + str(y) + '}'

    # draw walls
    for y, row in enumerate(map.map):
        for x, field in enumerate(row):
            if field == 'x':
                print '\BTwall{' + str(x) + '}{' + str(y) + '}'

    # draw traps
    for y, row in enumerate(map.map):
        for x, field in enumerate(row):
            if map.traps.isTrap(field):
                print '\BTtrap{' + str(x) + '}{' + str(y) + '}{' + field + '}'

    # draw path
    sys.stdout.write('\BTpath{')
    for i, cell in enumerate(path):
        if i != 0:
            sys.stdout.write(' -- ')
        sys.stdout.write('(' + str(cell.x) + '.5,' + str(cell.y) + '.5)')
    print '}'

    # draw "maybe" paths
    for maybepath in maybepaths:
        sys.stdout.write('\BTmaybepath{')
        for i, cell in enumerate(maybepath):
            if i != 0:
                sys.stdout.write(' -- ')
            sys.stdout.write('(' + str(cell.x) + '.5,' + str(cell.y) + '.5)')
        print '}'

    # draw "no" paths
    for nopath in nopaths:
        sys.stdout.write('\BTnopath{')
        for i, cell in enumerate(nopath):
            if i != 0:
                sys.stdout.write(' -- ')
            sys.stdout.write('(' + str(cell.x) + '.5,' + str(cell.y) + '.5)')
        print '}'

    # draw start
    for y, row in enumerate(map.map):
        for x, field in enumerate(row):
            if Cell(x, y, map.getAt(x, y)) == start:
                print '\BTstart{' + str(x) + '}{' + str(y) + '}'

    # draw end
    for y, row in enumerate(map.map):
        for x, field in enumerate(row):
            if Cell(x, y, map.getAt(x, y)) == end:
                print '\BTend{' + str(x) + '}{' + str(y) + '}'

    # draw grid
    print '\BTgrid{' + str(map.width) + '}{' + str(map.height) + '}'

    # draw coords
    if showCoords:
        print '\BTcoords{' + str(map.width) + '}{' + str(map.height) + '}'

    # draw graph
    if graph:
        for field in graph.graph:
            print '\BTnode{' + str(field.x) + '}{' + str(field.y) + '}'
            for adj in graph.graph[field]:
                print '\BTedge{' + str(field.x) + '}{' + str(field.y) + '}{' + str(adj.x) + '}{' + str(adj.y) + '}'

    print '}'


def uniqueTraps(map):
    """Return a sorted list of unique traps in the map, with '0' at the start to
    mark empty cells (if the map contains any).
    """
    traps = []

    # add '0' to the start of the traps list of the map contains any empty cells
    for y, row in enumerate(map.map):
        if traps:
            break  # sadly, breaking out of both loops at once seems impossible
        for x, field in enumerate(row):
            if not map.traps.isTrap(field) and not traps:
                traps = ['0']
                break

    # add traps
    for y, row in enumerate(map.map):
        for x, field in enumerate(row):
            if map.traps.isTrap(field):
                traps.append(field)

    # get rid of duplicates
    uniqueTraps = list(set(traps))

    return sorted(uniqueTraps)


def cellFormatString(cell, start, end, traps, neighbors, inaccessibleNeighbors, c):
    """Generate the format string for a cell (x, y)."""
    formatString = "({},{})"

    if cell == start:
        formatString = "\\textcolor{{\BTstartcolor}}{{" + formatString + "}}"
    elif cell == end:
        formatString = "\\textcolor{{\BTendcolor}}{{" + formatString + "}}"
    elif traps.isTrap(cell.value):
        formatString = "\\textcolor{{\BTtrapcolor}}{{" + formatString + "}}"

    if cell in neighbors:
        formatString = "\BTmaybeunderline{{" + formatString + "}}"
    elif cell in inaccessibleNeighbors:
        formatString = "\BTnounderline{{" + formatString + "}}"
    elif cell == c['cell']:
        formatString = "\BThighlighttext{{" + formatString + "}}"

    return formatString


def formatQueueFrame(qf, start, end, traps, neighbors, inaccessibleNeighbors, c):
    """Format a queue frame consisting of cell, path and maximum triggered trap:
    ((x1, y1), [(x2, y2), ..., (x3, y3), (x4, y4)], t).
    """

    # cell
    formatString = cellFormatString(qf['cell'], start, end, traps, neighbors, inaccessibleNeighbors, c)
    qfCell = formatString.format(qf['cell'].x, qf['cell'].y)

    # first element of path
    formatString = cellFormatString(qf['path'][0], start, end, traps, neighbors, inaccessibleNeighbors, c)
    qfPath = formatString.format(qf['path'][0].x, qf['path'][0].y)

    # dots indicating path longer than 3
    if (len(qf['path']) > 3):
        qfPath += ",\dots"

    # second-to-last element of path
    if (len(qf['path']) > 2):
        formatString = cellFormatString(qf['path'][-2], start, end, traps, neighbors, inaccessibleNeighbors, c)
        formatString = "," + formatString
        qfPath += formatString.format(qf['path'][-2].x, qf['path'][-2].y)

    # last element of path
    if (len(qf['path']) > 1):
        formatString = cellFormatString(qf['path'][-1], start, end, traps, neighbors, inaccessibleNeighbors, c)
        formatString = "," + formatString
        qfPath += ",({},{})".format(qf['path'][-1].x, qf['path'][-1].y)

    # maximum triggered trap
    qfTrap = traps.getValue(qf['triggered'])
    if traps.isTrap(qfTrap):
        qfTrap = "\\textcolor{\BTtrapcolor}{" + qfTrap + "}"

    return "(" + qfCell + ", [" + qfPath + "], " + qfTrap + ")"


# TODO improve alignment
# TODO improve separator
def generateSlide(map, traps, start, end, q, visited, c, neighbors, inaccessibleNeighbors, step, scale=1):
    """Ouput the source code of a single LaTeX Beamer slide."""

    print '\\begin{frame}'
    #print '\frametitle{Beispiel}'
    #print '\framesubtitle{Schritt ' + str(step-1) + ': TODO}'
    #print '\\begin{enumerate}'
    #print '\setcounter{enumi}{' + str(step-1) + '}'
    #print '\item TODO'
    #print '\end{enumerate}'
    print '\\begin{columns}[c,onlytextwidth]'
    print '\\begin{column}{.4\\textwidth}'

    # print map
    maybepaths = []
    for neighbor in neighbors:
        maybepaths.append([c['cell'], neighbor])
    nopaths = []
    for neighbor in inaccessibleNeighbors:
        nopaths.append([c['cell'], neighbor])
    printLatexMapDrawCommands(map, start, end, False, c['path'], maybepaths, nopaths, [c['cell']], scale, True)

    print '\end{column}'
    print '\hspace{1em}'
    print '\\begin{column}{.5\\textwidth}'
    print '\\begin{align*}'

    # print current queue frame
    if step > 1:
        print "\BTvphantomfix c_{" + str(step-1) + "} &= " + formatQueueFrame(c, start, end, traps, neighbors, inaccessibleNeighbors, c) + "\\\\"
        print "\midrule"

    # print visited sets
    for trap in uniqueTraps(map):
        formattedCells = []
        for visitedCell in visited[traps.getIndex(trap)]:
            formatString = cellFormatString(visitedCell, start, end, traps, neighbors, inaccessibleNeighbors, c)
            formattedCells.append(formatString.format(visitedCell.x, visitedCell.y))

        if not formattedCells:
            print '\BTvphantomfix v_' + str(trap) + ' &= \\varnothing\\\\'
        else:
            if len(formattedCells) > 4:
                del formattedCells[:-5]
                formattedCells[0] = "\dots"
            print '\BTvphantomfix v_' + str(trap) + ' &= \{' + ",".join(formattedCells) + '\}\\\\'

    # print first three elements of queue, truncating long paths in queue frames
    queueContents = []
    while not q.empty():
        queueContents.append(q.get())
    for qf in queueContents:
        q.put(qf)
    queueContentsFormatted = []
    for qf in queueContents:
        qfFormatted = formatQueueFrame(qf, start, end, traps, neighbors, inaccessibleNeighbors, c)
        queueContentsFormatted.append(qfFormatted)
    if len(queueContentsFormatted) > 3:
        del queueContentsFormatted[3:]
        queueContentsFormatted.append("\dots")
    print 'q &= [' + ",\\\\ \BTvphantomfix &\phantom{{}=[}".join(queueContentsFormatted) + ']'

    print '\end{align*}'
    print '\end{column}'
    print '\end{columns}'
    print '\end{frame}'


# TODO \relax\ifmmode\startedinmathmodetrue\else\startedinmathmodefalse\fi really necessary?
def raidTombAndGenerateBeamerSlides(graph, traps, start, end, map, scale):
    """Find the shortest path between start and end cells ("raid the tomb")
    using modified breadth-first search and output the source code of a LaTeX
    Beamer slide detailing each step.
    Please note that this is really only tested with sampleinput9.txt.
    Make sure to \input{boobytraps-latex-preample.tex} in your .tex file.
    """
    graph = graph.graph
    q = Queue.Queue()

    # initialize visited structure
    visited = {}
    visited[0] = []
    for i in traps.trapDominationLookup.values():
        visited[i] = []

    # add start to queue
    c = {'cell': start, 'path': [start], 'triggered': traps.getIndex(start.value)}
    visited[c['triggered']].append(c['cell'])
    q.put(c)

    # generate slide for initial state
    step = 1
    generateSlide(map, traps, start, end, q, visited, c, [], [], step, scale)

    while not q.empty():

        # get new cell
        c = q.get()

        neighbors = []
        inaccessibleNeighbors = []
        for neighbor in graph[c['cell']]:
            inaccessibleNeighbors.append(neighbor)

        # add eligible neighbors to queue and check if one of them is the end
        for neighbor in graph[c['cell']]:

            # make sure neighbor has not been visited yet
            neighborVisited = False
            if c['path'][0].value == 'o':
                neighborVisited = neighbor in visited[0]
            for d in c['path']:
                if neighborVisited:
                    break
                if d.value != 'o':
                    neighborVisited = neighborVisited or neighbor in visited[traps.getIndex(d.value)]

            if not neighborVisited:

                # make sure the neigbor can be visited and update maximum triggered trap
                triggered = c['triggered']
                if traps.isTrap(neighbor.value):
                    v = neighbor.value
                    if traps.getIndex(v) <= triggered:  # trap already in path
                        continue
                    triggered = traps.getIndex(v)

                # create new queue frame
                n = {'cell': neighbor, 'path': c['path'] + [neighbor], 'triggered': triggered}

                # move neighbor to list of accessible neighbors
                inaccessibleNeighbors.remove(neighbor)
                neighbors.append(neighbor)

                # check if the end has been reached
                if neighbor == end:

                    # generate second-to-last slide and show queue entry for end
                    q.put(n)
                    if neighbor not in visited[n['triggered']]:
                        visited[n['triggered']].append(neighbor)
                    step += 1
                    generateSlide(map, traps, start, end, q, visited, c, neighbors, inaccessibleNeighbors, step, scale)

                    # generate last slide with empty queue
                    step += 1
                    generateSlide(map, traps, start, end, Queue.Queue(), visited, n, [], [], step, scale)

                    return len(n['path']) - 1, n['path'], set().union(*visited.values())
                else:
                    q.put(n)
                    if neighbor not in visited[n['triggered']]:
                        visited[n['triggered']].append(neighbor)

        # generate slide
        step += 1
        generateSlide(map, traps, start, end, q, visited, c, neighbors, inaccessibleNeighbors, step, scale)

    # return longest/"best effort" path
    return -1, c['path'], set().union(*visited.values())


def main():
    # process options (hacky, i know)
    printMap = len(sys.argv) > 1 and sys.argv[1] == "--map"
    if printMap:
        del sys.argv[1]

    generateSlides = len(sys.argv) > 1 and sys.argv[1] == "--slides"
    if generateSlides:
        del sys.argv[1]

    if not printMap:
        printMap = len(sys.argv) > 1 and sys.argv[1] == "--map"
        if printMap:
            del sys.argv[1]

    # parse input
    traps, map, graph, start, end = parseInput(fileinput.input())

    # compute map scale factor appropriate for filling the left half of a beamer slide
    scale = min(4.0 / map.width, 4.0 / map.height)

    # raid the tomb and generate slides
    if generateSlides:
        raidTombAndGenerateBeamerSlides(graph, traps, start, end, map, scale)

    # raid the tomb and print the map
    if printMap:
        moves, path, visited = raidTomb(graph, traps, start, end)
        printLatexMapDrawCommands(map, start, end, False, path, [], [], [], scale, True)

if __name__ == "__main__":
    main()
