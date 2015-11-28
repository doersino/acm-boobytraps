# TODO

## `boobytraps.py`
* add docstrings
* refactor everything after cloning the map in raidtomb(): make sure it actually finds the shortest path and doesn't end in an infinite loop
* maybe return and prettyprint (with red background) the "best effort" if no path is found
* maybe change coords class to cell class with coords and value, change map accordingly
* maybe identify coords by integer, like width*y+x
* getAt, setAt neccessary, especially in the map class itself?

* use graph representation of map
	* collapse paths: o -> o -> o => o -2> o
	* graph nodes as cells with x, y, value, maybe bool: visited
* instead of entire map, pass max triggered trap, then ignore all traps <= max

## `tombraider.sh`

## `gravedigger.sh`
* generate more traps on mid-size maps
* option for start/end: --start X,Y --end X,Y, make sure to set to o
* otherwise random but with minimum euclidean distance, and: if start/end is 'x', generate new position
* option for ratio of wall cells to empty cells ("density"? in [0, 1], default .5) => allows removal of magic numbers
* option to output seed (make sure to output auto-generated seeds accurately)
