#!/usr/bin/python2.7

# Using boobytraps.py, generates LaTeX snippets related to boobytraps.py:
# If the --map option is given, this script prints the draw commands for a LaTeX
# representation of the map (using tikz).
# If the --slides option is given, this script prints the source code of beamer
# slides detailing all steps of the path finding algorithm.
#
# Usage: Either of the following three options will work:
#
#        ./boobytraps-latex.py [--map] [--slides] INPUT_FILE
#        cat INPUT_FILE | ./boobytraps-latex.py [--map] [--slides]
#        ./gravedigger.py WIDTH HEIGHT | ./boobytraps-latex.py [--map] [--slides]

from boobytraps import *


# TODO change macros to have fewer args
def printLatexMapDrawCommands(map, start, end, path=[], maybepaths=[], nopaths=[], highlight=[], scale=1, showCoords=False):
    """Quick-and-dirty way of printing the draw commands for a LaTeX
    representation of the map (using tikz).
    If you want to highlight an incorrect path, change \BTpath to \BTpathX
    in the output of this function, and if you want to highlight a cell, use
    the \BThighlight macro.
    The following macros need to be defined in the preamble of your LaTeX
    document:

    \def\BThighlightcolor{yellow}
    \def\BTwallcolor{gray}
    \def\BTtrapcolor{red}
    \def\BTpathcolor{green!60!black}
    \let\BTmaybepathcolor\BTpathcolor
    \def\BTnopathcolor{red!60!black}
    \def\BTstartcolor{blue!85!black}
    \def\BTendcolor{red!75!black}

    \newcommand{\BTmap}[2]{ % scale factor & draw commands
        \begin{center}
            \begin{tikzpicture}[scale=#1,every node/.style={transform shape}]
                #2
            \end{tikzpicture}
        \end{center}
    }
    \newcommand{\BThighlight}[2]{ % bottom left corner & top right corner
        \fill[\BThighlightcolor] (#1) rectangle (#2);
    }
    \newcommand{\BTwall}[2]{ % bottom left corner & top right corner
        \fill[\BTwallcolor] (#1) rectangle (#2);
    }
    \newcommand{\BTtrap}[2]{ % position & letter
        \node at (#1) {\LARGE\bfseries\color{\BTtrapcolor} #2};
    }
    \newcommand{\BTpath}[1]{ % path
        \draw[\BTpathcolor, solid, very thick] #1;
    }
    \newcommand{\BTmaybepath}[1]{ % path
        \draw[\BTmaybepathcolor, dotted, very thick] #1;
    }
    \newcommand{\BTnopath}[1]{ % path
        \draw[\BTnopathcolor, dotted, very thick] #1;
    }
    \newcommand{\BTstart}[1]{ % position
        \path[fill=\BTstartcolor] (#1) circle (0.25);
    }
    \newcommand{\BTend}[1]{ % position
        \path[fill=\BTendcolor] (#1) circle (0.25);
    }
    \newcommand{\BTgrid}[1]{ % width,height
        \draw[step=1,black,thick] (0,0) grid (#1);
    }
    \newcommand{\BTcoords}[2]{ % width & height
        \foreach \nx in {0,...,\numexpr#1-1\relax}
            \foreach \my in {0,...,\numexpr#2-1\relax}
                \node[anchor=west,inner sep=0] at (\nx+0.05,#2-\my-0.18) {\tiny(\nx,\my)};
    }
    """

    print '\BTmap{' + str(scale) + '}{'

    # draw highlights
    for y, row in enumerate(map.map):
        for x, field in enumerate(row):
            if Cell(x, y, map.getAt(x, y)) in highlight:
                print '\BThighlight{' + str(x) + ',' + str(map.height-y) + '}{' + str(x+1) + ',' + str(map.height-(y+1)) + '}'

    # draw walls
    for y, row in enumerate(map.map):
        for x, field in enumerate(row):
            if field == 'x':
                print '\BTwall{' + str(x) + ',' + str(map.height-y) + '}{' + str(x+1) + ',' + str(map.height-(y+1)) + '}'

    # draw traps
    for y, row in enumerate(map.map):
        for x, field in enumerate(row):
            if map.traps.isTrap(field):
                print '\BTtrap{' + str(x) + '.5,' + str(map.height-(y+1)) + '.5}{' + field + '}'

    # draw "maybe" paths
    for maybepath in maybepaths:
        sys.stdout.write('\BTmaybepath{')
        for i, cell in enumerate(maybepath):
            if i != 0:
                sys.stdout.write(' -- ')
            sys.stdout.write('(' + str(cell.x) + '.5,' + str(map.height-(cell.y+1)) + '.5)')
        print '}'

    # draw "no" paths
    for nopath in nopaths:
        sys.stdout.write('\BTnopath{')
        for i, cell in enumerate(nopath):
            if i != 0:
                sys.stdout.write(' -- ')
            sys.stdout.write('(' + str(cell.x) + '.5,' + str(map.height-(cell.y+1)) + '.5)')
        print '}'

    # draw path
    sys.stdout.write('\BTpath{')
    for i, cell in enumerate(path):
        if i != 0:
            sys.stdout.write(' -- ')
        sys.stdout.write('(' + str(cell.x) + '.5,' + str(map.height-(cell.y+1)) + '.5)')
    print '}'

    # draw start
    for y, row in enumerate(map.map):
        for x, field in enumerate(row):
            if Cell(x, y, map.getAt(x, y)) == start:
                print '\BTstart{' + str(x) + '.5,' + str(map.height-(y+1)) + '.5}'

    # draw end
    for y, row in enumerate(map.map):
        for x, field in enumerate(row):
            if Cell(x, y, map.getAt(x, y)) == end:
                print '\BTend{' + str(x) + '.5,' + str(map.height-(y+1)) + '.5}'

    # draw grid
    print '\BTgrid{' + str(map.width) + ',' + str(map.height) + '}'

    # draw coords
    if showCoords:
        print '\BTcoords{' + str(map.width) + '}{' + str(map.height) + '}'

    print '}'


def uniqueTraps(map):
    """Return a sorted list of unique traps in the map."""
    traps = []

    for y, row in enumerate(map.map):
        for x, field in enumerate(row):
            if map.traps.isTrap(field):
                traps.append(field)

    uniqueTraps = list(set(traps))

    return sorted(uniqueTraps)


def generateSlide(map, traps, start, end, q, visited, c, neighbors, inaccessibleNeighbors, step, scale=1):
    # TODO highlight c (yellow background) and neighbors (dotted underline) in sets, queue
    # TODO highlight start, end
    # TODO highlight traps
    # TODO blue or grey paths (on top of other paths) to visited but otherwise accessible cells (visitedNeighbors)?

    print
    print '\\begin{frame}'
    #print '\frametitle{Implementation}'
    #print '\framesubtitle{Beispiel}'
    print '\\begin{enumerate}'
    print '\setcounter{enumi}{' + str(step-1) + '}'
    print '\item TODO'
    print '\end{enumerate}'
    print '\\begin{columns}[c]'
    print '\\begin{column}{.4\\textwidth}'

    # print map
    maybepaths = []
    for neighbor in neighbors:
        maybepaths.append([c['cell'], neighbor])
    nopaths = []
    for neighbor in inaccessibleNeighbors:
        nopaths.append([c['cell'], neighbor])
    printLatexMapDrawCommands(map, start, end, c['path'], maybepaths, nopaths, [c['cell']], scale, True)

    print '\end{column}'
    print '\\begin{column}{.5\\textwidth}'
    print '\\begin{align*}'

    # print visited set for empty fields
    a3 = ["({},{})".format(a1.x, a1.y) for a1 in visited[0]]
    if not a3:
        print 'v_0 &= \\varnothing\\\\'
    else:
        print 'v_0 &= \{' + ",".join(a3) + '\}\\\\'

    # print visited sets for traps
    for a2 in uniqueTraps(map):
        a3 = ["({},{})".format(a1.x, a1.y) for a1 in visited[traps.trapDominationLookup[a2]]]
        if not a3:
            print 'v_' + str(a2) + ' &= \\varnothing\\\\'
        else:
            print 'v_' + str(a2) + ' &= \{' + ",".join(a3) + '\}\\\\'

    # print queue, truncating long paths in queue frames
    queueContents = []
    while not q.empty():
        queueContents.append(q.get())
    for qf in queueContents:
        q.put(qf)
    queueContentsFormatted = []
    for qf in queueContents:
        qfCell = "({},{})".format(qf['cell'].x, qf['cell'].y)
        qfPath = "({},{})".format(qf['path'][0].x, qf['path'][0].y)
        if (len(qf['path']) > 3):
            qfPath += ",\dots"
        if (len(qf['path']) > 2):
            qfPath += ",({},{})".format(qf['path'][-2].x, qf['path'][-2].y)
        if (len(qf['path']) > 1):
            qfPath += ",({},{})".format(qf['path'][-1].x, qf['path'][-1].y)
        qfTrap = traps.getValue(qf['triggered'])
        queueContentsFormatted.append("(" + qfCell + ", [" + qfPath + "], " + qfTrap)
    print 'q &= (' + ",\\\\&".join(queueContentsFormatted) + ')'

    print '\end{align*}'
    print '\end{column}'
    print '\end{columns}'
    print '\end{frame}'


def raidTombAndGenerateBeamerSlides(graph, traps, start, end, map, scale):
    """Find the shortest path between start and end cells ("raid the tomb")
    using modified breadth-first search and output a LaTeX beamer slide
    detailing each step.
    Note that this is really only tested with sampleinput9.txt.
    Copy the macros from the printLatexMapDrawCommands() docstring into your
    LaTeX preamble, which should also contain at least the following commands:

    \documentclass{beamer}
    \usepackage{multicol}
    \usepackage{tikz}

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

    step = 1
    generateSlide(map, traps, start, end, q, visited, c, [], [], step, scale)

    while not q.empty():

        # get new cell
        c = q.get()

        neighbors = []
        inaccessibleNeighbors = []
        for neighbor in graph[c['cell']]:
            #if neighbor not in c['path']:
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

                inaccessibleNeighbors.remove(neighbor)
                neighbors.append(neighbor)

                # check if the end has been reached
                if neighbor == end:
                    # TODO on second-to-last slide show queue entry
                    step += 1
                    generateSlide(map, traps, start, end, q, visited, c, neighbors, inaccessibleNeighbors, step, scale)
                    step += 1
                    generateSlide(map, traps, start, end, q, visited, n, [], [], step, scale)

                    return len(n['path']) - 1, n['path'], set().union(*visited.values())
                else:
                    q.put(n)
                    visited[n['triggered']].append(neighbor)

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

    # map scale factor (default fills half a beamer slide)
    scale = min(4.0 / map.width, 4.0 / map.height)

    # raid the tomb and generate slides
    if generateSlides:
        raidTombAndGenerateBeamerSlides(graph, traps, start, end, map, scale)

    # raid the tomb and print the map
    if printMap:
        moves, path, visited = raidTomb(graph, traps, start, end)
        printLatexMapDrawCommands(map, start, end, path, [], [], [], scale, True)

if __name__ == "__main__":
    main()
