#!/usr/bin/python2.7

# Using boobytraps.py, generates LaTeX snippets related to boobytraps.py:
# If the --map option is given, this script prints the draw commands for a LaTeX
# representation of the map and path (using tikz).
# If the --slides option is given, this script prints the source code of beamer
# slides detailing all steps of the path finding algorithm.
#
# Usage: Either of the following three options will work:
#
#        ./boobytraps-latex.py [--map] [--slides] INPUT_FILE
#        cat INPUT_FILE | ./boobytraps-latex.py [--map] [--slides]
#        ./gravedigger.py WIDTH HEIGHT | ./boobytraps-latex.py [--map] [--slides]

from boobytraps import *


# TODO add more options, use subparsers http://stackoverflow.com/questions/21287828/python-argparse-add-mutually-exclusive-group-need-ether-2-args-or-just-1-args
# TODO move macros etc. to preamble.tex file
# TODO improve path macro
# TODO update docstring with options, graph drawing
def printLatexMapDrawCommands(map, start, end, graph=False, path=[], maybepaths=[], nopaths=[], highlight=[], scale=1, showCoords=False):
    """Quick-and-dirty way of printing the draw commands for a LaTeX
    representation of the map (using tikz).
    If you want to highlight an incorrect path, change \BTpath to \BTnopath
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
    \def\BTnodecolor{black}
    \def\BTedgecolor{black}

    \newcommand{\BTmap}[2]{ % scale factor, draw commands
        \begin{center}
            \begin{tikzpicture}[y=-1cm,scale=#1,every node/.style={transform shape}]
                #2
            \end{tikzpicture}
        \end{center}
    }
    \newcommand{\BThighlight}[2]{ % x, y
        \fill[\BThighlightcolor] (#1,#2) rectangle (#1+1,#2+1);
    }
    \newcommand{\BTwall}[2]{ % x, y
        \fill[\BTwallcolor] (#1,#2) rectangle (#1+1,#2+1);
    }
    \newcommand{\BTtrap}[3]{ % x, y, char
        \node at (#1+0.5,#2+0.5) {\LARGE\bfseries\color{\BTtrapcolor} #3};
    }
    \newcommand{\BTpath}[1]{ % (x1,y1) -- ... -- (xn,yn)
        \draw[\BTpathcolor, solid, very thick] #1;
    }
    \newcommand{\BTmaybepath}[1]{ % (x1,y1) -- ... -- (xn,yn)
        \draw[\BTmaybepathcolor, dotted, very thick] #1;
    }
    \newcommand{\BTnopath}[1]{ % (x1,y1) -- ... -- (xn,yn)
        \draw[\BTnopathcolor, dotted, very thick] #1;
    }
    \newcommand{\BTstart}[2]{ % x, y
        \path[fill=\BTstartcolor] (#1+0.5,#2+0.5) circle (0.25);
    }
    \newcommand{\BTend}[2]{ % x, y
        \path[fill=\BTendcolor] (#1+0.5,#2+0.5) circle (0.25);
    }
    \newcommand{\BTgrid}[2]{ % width, height
        \draw[xstep=1,ystep=-1,black,thick] (0,0) grid (#1,#2);
    }
    \newcommand{\BTcoords}[2]{ % width, height
        \foreach \nx in {0,...,\numexpr#1-1\relax}
            \foreach \my in {0,...,\numexpr#2-1\relax}
                \node[anchor=west,inner sep=0] at (\nx+0.05,\my+0.18) {\tiny(\nx,\my)};
    }
    \newcommand{\BTnode}[2]{ % x, y
        \path[fill=\BTnodecolor] (#1+0.8,#2+0.8) circle (0.125);
    }
    \newcommand{\BTedge}[4]{ % first node position & second node position
        \draw[\BTedgecolor, solid, very thick] (#1+0.8,#2+0.8) -- (#3+0.8,#4+0.8);
    }
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


def generateSlide(map, traps, start, end, q, visited, c, neighbors, inaccessibleNeighbors, step, scale=1):
    # TODO highlight start, end cells (x, y) w/ prev defined colors
    # TODO highlight trap cells (x, y) w prev def colors

    print '\\begin{frame}'
    #print '\frametitle{Implementation}'
    #print '\framesubtitle{Beispiel}'
    print '\\begin{enumerate}'
    print '\setcounter{enumi}{' + str(step-1) + '}'
    print '\item TODO'
    print '\end{enumerate}'
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

    # print visited sets
    for trap in uniqueTraps(map):
        formattedCells = []
        for visitedCell in visited[traps.getIndex(trap)]:
            if visitedCell in neighbors:
                formatString = "\BTmaybeunderline{{({},{})}}"
            elif visitedCell in inaccessibleNeighbors:
                formatString = "\BTnounderline{{({},{})}}"
            elif visitedCell == c['cell']:
                formatString = "\BThighlighttext{{({},{})}}"
            else:
                formatString = "({},{})"
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

        # cell
        if qf['cell'] in neighbors:
            formatString = "\BTmaybeunderline{{({},{})}}"
        elif qf['cell'] in inaccessibleNeighbors:
            formatString = "\BTnounderline{{({},{})}}"
        elif qf['cell'] == c['cell']:
            formatString = "\BThighlighttext{{({},{})}}"
        else:
            formatString = "({},{})"
        qfCell = formatString.format(qf['cell'].x, qf['cell'].y)

        # first element of path
        if qf['path'][0] in neighbors:
            formatString = "\BTmaybeunderline{{({},{})}}"
        elif qf['path'][0] in inaccessibleNeighbors:
            formatString = "\BTnounderline{{({},{})}}"
        elif qf['path'][0] == c['cell']:
            formatString = "\BThighlighttext{{({},{})}}"
        else:
            formatString = "({},{})"
        qfPath = formatString.format(qf['path'][0].x, qf['path'][0].y)

        # dots indicating path longer than 3
        if (len(qf['path']) > 3):
            qfPath += ",\dots"

        # second-to-last element of path
        if (len(qf['path']) > 2):
            if qf['path'][-2] in neighbors:
                formatString = ",\BTmaybeunderline{{({},{})}}"
            elif qf['path'][-2] in inaccessibleNeighbors:
                formatString = ",\BTnounderline{{({},{})}}"
            elif qf['path'][-2] == c['cell']:
                formatString = ",\BThighlighttext{{({},{})}}"
            else:
                formatString = ",({},{})"
            qfPath += formatString.format(qf['path'][-2].x, qf['path'][-2].y)

        # last element of path
        if (len(qf['path']) > 1):
            if qf['path'][-1] in neighbors:
                formatString = ",\BTmaybeunderline{{({},{})}}"
            elif qf['path'][-1] in inaccessibleNeighbors:
                formatString = ",\BTnounderline{{({},{})}}"
            elif qf['path'][-1] == c['cell']:
                formatString = ",\BThighlighttext{{({},{})}}"
            else:
                formatString = ",({},{})"
            qfPath += ",({},{})".format(qf['path'][-1].x, qf['path'][-1].y)

        # maximum triggered trap
        qfTrap = traps.getValue(qf['triggered'])
        if traps.isTrap(qfTrap):
            qfTrap = "\\textcolor{\BTtrapcolor}{" + qfTrap + "}"

        queueContentsFormatted.append("(" + qfCell + ", [" + qfPath + "], " + qfTrap + ")")
    if len(queueContentsFormatted) > 3:
        del queueContentsFormatted[3:]
        queueContentsFormatted.append("\dots")
    print 'q &= [' + ",\\\\ \BTvphantomfix &\phantom{{}=[}".join(queueContentsFormatted) + ']'

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

    \newif\ifstartedinmathmode
    \newcommand*{\BTmaybeunderline}[1]{
        \relax\ifmmode\startedinmathmodetrue\else\startedinmathmodefalse\fi
        \tikz[baseline=(underlined.base)]{
            \node[inner sep=1pt,outer sep=0pt] (underlined) {\ifstartedinmathmode$#1$\else#1\fi};
            \draw[\BTmaybepathcolor,dotted,line width=1.16pt] (underlined.south west) -- (underlined.south east);
        }
    }

    \newcommand*{\BTnounderline}[1]{
        \relax\ifmmode\startedinmathmodetrue\else\startedinmathmodefalse\fi
        \tikz[baseline=(underlined.base)]{
            \node[inner sep=1pt,outer sep=0pt] (underlined) {\ifstartedinmathmode$#1$\else#1\fi};
            \draw[\BTnopathcolor,dotted,line width=1.16pt] (underlined.south west) -- (underlined.south east);
        }
    }

    \newcommand*{\BThighlighttext}[1]{
        \relax\ifmmode\startedinmathmodetrue\else\startedinmathmodefalse\fi
        \tikz[baseline=(highlighted.base)]{
            \node[rectangle,fill=\BThighlightcolor,inner sep=1.16pt] (highlighted) {\ifstartedinmathmode$#1$\else#1\fi};
        }
    }

    \newcommand*{\BTvphantomfix}{
        \vphantom{\BTmaybeunderline{(0,0)}\BTnounderline{(0,0)}\BThighlighttext{(0,0)}[],()}
    }

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
