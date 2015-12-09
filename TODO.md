# TODO

## `boobytraps.py`
* optimize graph: collapse paths: o -> o -> o => o -2> o, possibly remove deadends (if != start, end) => save start, end in map
* clean up
* add comments
* test by periodically prettyprinting the path
* mark fields as visited (because "shortest path" visits them first) so they won't be visited twice => might not work due to traps, but will work at least as long as no traps have been encountered at all yet => or maybe one per trap type (max len(trapDominationOrder))
* improve efficiency by using list or object instead of dict for queue frames
* if no graph optimizations: costs are all 1, so simplify graph structure
* return and prettyprint (with red background) the "best effort" (longest attempt, or one that got closest to end) if no path is found
* rework main function

* maybe use a faster language?

## `tombraider.sh`

## `gravedigger.sh`
