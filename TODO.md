# TODO

## `boobytraps.py`
* optimize graph: collapse paths: o -> o -> o => o -2> o, possibly remove deadends (if != start, end) => save start, end in map
* clean up
* add comments
* mark fields as visited (because "shortest path" visits them first) so they won't be visited twice => might not work due to traps, but will work at least as long as no traps have been encountered at all yet
* improve efficiency by using list or object instead of dict for queue frames
* return and prettyprint (with red background) the "best effort" (longest attempt, or one that got closest to end) if no path is found
* rework main function

* maybe use a faster language?

## `tombraider.sh`

## `gravedigger.sh`
