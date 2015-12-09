# TODO

## `boobytraps.py`
* optimize graph: collapse paths: o -> o -> o => o -2> o, possibly remove deadends (if != start, end) => save start, end in map
* try to get by without copy.deepcopy()
* instead of entire map/graph, pass max triggered trap, then ignore all traps <= max
* return and prettyprint (with red background) the "best effort" (longest attempt, or one that got closest to end) if no path is found

* if other approach fails, use simple iterative breadth-first search with backtracking, with triggered traps saved in queue along with cell
* improve efficiency by using list or object instead of dict for queue frames

## `tombraider.sh`

## `gravedigger.sh`
