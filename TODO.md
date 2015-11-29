# TODO

## `boobytraps.py`
* use graph representation of map
    * optimize: collapse paths: o -> o -> o => o -2> o
    * optimize: remove deadends (if != start, end) => save start, end in map
    * graph nodes as cells with x, y, value
* instead of entire map/graph, pass max triggered trap, then ignore all traps <= max
* add docstrings
* return and prettyprint (with red background) the "best effort" if no path is found

* if other approach fails, use simple iterative breadth-first search with backtracking, with triggered traps saved in queue along with cell

## `tombraider.sh`

## `gravedigger.sh`
* generate more traps on mid-size maps
* option for start/end: --start X,Y --end X,Y, make sure to set to o
* otherwise random but with minimum euclidean distance, and: if start/end is 'x', generate new position
* option for ratio of wall cells to empty cells ("density"? in [0, 1], default .5) => allows removal of magic numbers
* option to output seed (make sure to output auto-generated seeds accurately)
