# TODO

## `boobytraps.py`
* optimize graph: collapse paths: o -> o -> o => o -2> o, possibly remove deadends (if != start, end) => save start, end in map
* clean up
* add comments
* test by periodically prettyprinting the path
* improve efficiency by using list or object instead of dict for queue frames
* if no graph optimizations: costs are all 1, so simplify graph structure => adj list?
* return and prettyprint (with red background) the "best effort" (longest attempt, or one that got closest to end) if no path is found, which is easy because it's the last element of the queue
* rework main function

* maybe use a faster language?

## `gravedigger.sh`

## `tombraider.sh`

## `sampleinput5.txt`
* maybe luke starting somewhere near the bottom right, separated by death ray
