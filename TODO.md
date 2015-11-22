# TODO

## `boobytraps.py`
* add docstrings
* fix "IMPOSSIBLE" output
* refactor everything after cloning the map in raidtomb()
* maybe change coords class to cell class with coords and value, change map accordingly
* maybe identify coords by integer, like width*y+x
* getAt, setAt neccessary, especially in the map class itself?
* maybe add -v flag with colorized map with coord axes, as well as path output after each step

* use graph representation of map
	* collapse paths: o -> o -> o => o -2> o
	* graph nodes as cells with x, y, value, maybe bool: visited
* instead of entire map, pass max triggered trap, then ignore all traps <= max
* build data generator for large maps

## `tombraider.sh`
* dynamically determine if input and output given are files or plaintext
* don't compare with example if -v flag?

## `gravedigger.sh`
* generate interesting maps: place lines, boxes
* option for start/end: --start X,Y --end X,Y, otherwise random?
* if start/end is 'x', generate new position
* option for ratio of wall cells to empty cells, remove magic number
* generate multiple traps of same kind
