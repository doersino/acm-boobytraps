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


def printLatexMapDrawCommands(map, start, end, path=[], highlight=[], highlightalt=[], scale=1, showCoords=False):
    """Quick-and-dirty way of printing the draw commands for a LaTeX
    representation of the map (using tikz).
    If you want to highlight an incorrect path, change \BTpath to \BTpathX
    in the output of this function, and if you want to highlight a cell, use
    the \BThighlight macro.
    The following macros need to be defined in the preamble of your LaTeX
    document:

    \def\BThighlightcolor{yellow}
    \def\BThighlightaltcolor{green!60!white}
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
    \newcommand{\BThighlight}[2]{ % bottom left corner & top right corner
        \fill[\BThighlightcolor] (#1) rectangle (#2);
    }
    \newcommand{\BThighlightalt}[2]{ % bottom left corner & top right corner
        \fill[\BThighlightaltcolor] (#1) rectangle (#2);
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
    for y, row in enumerate(map.map):
        for x, field in enumerate(row):
            if Cell(x, y, map.getAt(x, y)) in highlightalt:
                print '\BThighlightalt{' + str(x) + ',' + str(map.height-y) + '}{' + str(x+1) + ',' + str(map.height-(y+1)) + '}'

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


def trapValue(traps, trap):
    if trap > 0:
        return traps.trapDominationOrder[trap-1]
    return str(0)


def generateSlide(map, traps, start, end, q, visited, c, neighbors, step, scale=1):
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
    printLatexMapDrawCommands(map, start, end, c['path'], neighbors, [c['cell']], scale, True)  # TODO print red dotted path to non-accessible cells (visited, tdo, etc.), green dotted path to possible cells
    print '\end{column}'
    print '\\begin{column}{.5\\textwidth}'
    print '\\begin{align*}'
    a3 = ["({},{})".format(a1.x, a1.y) for a1 in visited[0]]
    if not a3:
        print 'v_0 &= \\varnothing\\\\'
    else:
        print 'v_0 &= \{' + ",".join(a3) + '\}\\\\'
    for a2 in uniqueTraps(map):
        a3 = ["({},{})".format(a1.x, a1.y) for a1 in visited[traps.trapDominationLookup[a2]]]
        if not a3:
            print 'v_' + str(a2) + ' &= \\varnothing\\\\'
        else:
            print 'v_' + str(a2) + ' &= \{' + ",".join(a3) + '\}\\\\'
    queueContents = []
    while not q.empty():
        queueContents.append(q.get())
    for qf in queueContents:
        q.put(qf)
    # TODO truncate queue path contents like 1, ..., n-1, n for output
    print 'q &= (' + ",\\\\&".join(["(({},{}), [".format(qf['cell'].x, qf['cell'].y) + ",".join(["({},{})".format(a4.x, a4.y) for a4 in qf['path']]) + "], " + trapValue(traps, qf['triggered']) for qf in queueContents]) + ')'  # TODO proper output
    print '\end{align*}'
    print '\end{column}'
    print '\end{columns}'
    print '\end{frame}'


def raidTombAndGenerateBeamerSlides(graph, traps, start, end, map, scale):
    """Find the shortest path between start and end cells ("raid the tomb")
    using modified breadth-first search and output a LaTeX beamer slide
    detailing each step.
    Copy the macros from the printLatexMapDrawCommands() docstring into your
    LaTeX preamble, which should contain the following commands (along with
    title slide etc.):

    \documentclass{beamer}
    \usepackage{multicol}
    \usepackage{tikz}
    [macros]

    """
    graph = graph.graph
    q = Queue.Queue()

    # initialize visited structure
    visited = {}
    visited[0] = []
    for i in traps.trapDominationLookup.values():
        visited[i] = []  # TODO benchmark if lists are faster in normal version as well

    # add start to queue
    if traps.isTrap(start.value):
        c = {'cell': start, 'path': [start], 'triggered': traps.getIndex(start.value)}
        visited[c['triggered']].append(c['cell'])
    else:
        c = {'cell': start, 'path': [start], 'triggered': 0}
        visited[0].append(c['cell'])
    q.put(c)

    step = 1
    generateSlide(map, traps, start, end, q, visited, c, [], step, scale)

    while not q.empty():
        neighbors = []

        # get new cell
        c = q.get()

        # TOOD rm
        #print
        #print "<- {'cell': " + str(c['cell']) + ", 'path': [" + ", ".join(["(" + str(d) + ")" for d in c['path']]) + "], 'triggered': " + str(c['triggered']) + "}"
        #print "0: " + ", ".join(["(" + str(d) + ")" for d in visited[0]])
        #print "A: " + ", ".join(["(" + str(d) + ")" for d in visited[26]])
        #print "B: " + ", ".join(["(" + str(d) + ")" for d in visited[25]])

        for neighbor in graph[c['cell']]:
            if neighbor not in c['path']:
                neighbors.append(neighbor)

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

                # check if the end has been reached
                if neighbor == end:
                    # TODO print with c
                    step += 1
                    generateSlide(map, traps, start, end, q, visited, c, neighbors, step, scale)
                    # TODO print with n
                    return len(n['path']) - 1, n['path'], set().union(*visited.values())
                else:
                    q.put(n)
                    visited[n['triggered']].append(neighbor)

                    # TOOD rm
                    #print "-> {'cell': " + str(n['cell']) + ", 'path': [" + ", ".join(["(" + str(d) + ")" for d in n['path']]) + "], 'triggered': " + str(n['triggered']) + "}"
                    #print "v[" + str(n['triggered']) + "] <- " + str(neighbor)

        # TODO print
        step += 1
        generateSlide(map, traps, start, end, q, visited, c, neighbors, step, scale)

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
    scale = min(3.2 / map.width, 4.0 / map.height)

    # raid the tomb and generate slides
    if generateSlides:
        raidTombAndGenerateBeamerSlides(graph, traps, start, end, map, scale)

    # raid the tomb and print the map
    if printMap:
        moves, path, visited = raidTomb(graph, traps, start, end)
        printLatexMapDrawCommands(map, start, end, path, [], [], scale, True)

if __name__ == "__main__":
    main()
