# TODO

* add docstrings
* fix "IMPOSSIBLE" output
* refactor everything after cloning the map in raidtomb()
* maybe change coords class to cell class with coords and value, change map accordingly
* maybe identify coords by integer, like width*y+x
* getAt, setAt neccessary, especially in the map class itself?
* maybe add -v flag with colorized map with coord axes, as well as path output after each step

* use graph representation of map
	* collapse paths: o -> o -> o => o -2> o
* instead of entire map, pass max triggered trap, then ignore all traps <= max
* build data generator for large maps
