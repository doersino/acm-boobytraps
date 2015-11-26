# TODO

## `boobytraps.py`
* add docstrings
* refactor everything after cloning the map in raidtomb(): make sure it actually finds the shortest path
* maybe return and prettyprint (with red background) the "best effort" if no path is found
* maybe change coords class to cell class with coords and value, change map accordingly
* maybe identify coords by integer, like width*y+x
* getAt, setAt neccessary, especially in the map class itself?

* use graph representation of map
	* collapse paths: o -> o -> o => o -2> o
	* graph nodes as cells with x, y, value, maybe bool: visited
* instead of entire map, pass max triggered trap, then ignore all traps <= max
* build data generator for large maps

## `tombraider.sh`
* dynamically determine if input and output given are files or plaintext
* don't compare with example if -v flag?

## `gravedigger.sh`
* option for start/end: --start X,Y --end X,Y, make sure to set to o
* otherwise random but with minimum euclidean distance, and: if start/end is 'x', generate new position
* option for ratio of wall cells to empty cells ("density"? in [0, 1], default .5) => allows removal of magic numbers
* option to output seed (make sure to output auto-generated seeds accurately)
