# acm-boobytraps

My Python 2.7 solution of the ACM Programming Contest problem ["Booby Traps"](https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&category=258&page=show_problem&problem=1649), created as part of my assignment for the ["Selected Fun Problems of the ACM Programming Contest" proseminar](http://db.inf.uni-tuebingen.de/teaching/SelectedFunProblemsoftheACMProgrammingContest-Proseminar-WS2015-2016.html) at Uni Tübingen during the 2015 fall semester.

![screenshot](https://github.com/doersino/acm-boobytraps/raw/master/screenshot.png)

## Table of Contents
Books have one, so why shouldn't software?

* `boobytraps.py` contains the code solving the problem.
* `gravedigger.py` is a simple map generator I wrote for testing the performance of `boobytraps.py` on large maps. Run it with the `-h` flag to find out how to use it.
* `sampleinput.txt` contains the sample input with which to test the solution.
* `sampleinput[0-9]+.txt` contain other interesting sample inputs.
* `sampleoutput.txt` contains the sample output with which to test the solution.
* `screenshot.png` shows my shortest path finder in action on the sample input.
* `screenshot2.png` shows my map generator and shortest path finder in action.
* `tombraider.sh` is a short shell script for efficiently testing the solution.

## Example Usage

### `tombraider.sh`

Test the shortest path finder on the sample input and output given with the problem statement:
```
./tombraider.sh -i sampleinput.txt -o sampleoutput.txt
```

Test the shortest path finder on another sample input, specifying the expected output directly:
```
./tombraider.sh -i sampleinput2.txt -o 2
```

Test the shortest path finder on a third, more complex sample input:
```
./tombraider.sh -i sampleinput4.txt
```


### `boobytraps.py`
Run the shortest path finder on the sample input given with the problem statement (any of the four lines of code below will do this):
```
cat sampleinput.txt | python boobytraps.py
cat sampleinput.txt | ./boobytraps.py
python boobytraps.py sampleinput.txt
./boobytraps.py sampleinput.txt
```

For verbose output (this will highlight the path in the map), use the `-v` flag:
```
cat sampleinput.txt | python boobytraps.py -v
cat sampleinput.txt | ./boobytraps.py -v
python boobytraps.py -v sampleinput.txt
./boobytraps.py -v sampleinput.txt
```

### `gravedigger.py`

Randomly generate a 15x15 map and find the shortest path from start to end:
```
./gravedigger.py 15 15 | ./boobytraps.py
```

Randomly generate a 15x10 map (with a fixed seed, using the "dungeon" mode and with start and end in the top left and bottom right corners), find the shortest path from start to end and highlight the path in the map:
```
./gravedigger.py 15 10 --seed donghwa --mode dungeon --start 0,0 --end 14,9 | ./boobytraps.py -v
```

Randomly generate a large map (with a fixed seed, using the "dungeon" mode and a high map complexity), find the shortest path from start to end and highlight the path in the map:
```
./gravedigger.py 78 40 --seed donghwa --complexity 15 --mode dungeon | ./boobytraps.py -v
```

Randomly generate 40x20 maps (using the "dungeon" mode) until one with a shortest path from start to end is found, then highlight this path in the map, also output the time taken for each map generation/path finding attempt:
```
false; while [ $? -ne 0 ]; do time ./gravedigger.py 40 20 --mode dungeon | ./boobytraps.py -v; done
```

Randomly generate giant 202x51 maps (using the "dungeon" mode and higher-than normal map complexity) and print the random seed used for map generation until one with a shortest path from the upper left cell to the lower right cell is found, then highlight this path in the map, also output the time taken for each map generation/path finding attempt:
```
false; while [ $? -ne 0 ]; do time ./gravedigger.py 202 51 --printseed --complexity 15 --mode dungeon --start 0,0 --end 201,50 | ./boobytraps.py -v; done
```

![screenshot2](https://github.com/doersino/acm-boobytraps/raw/master/screenshot2.png)

As above, but with even larger 200x200 maps and additional highlighting of visited fields as well as the "best effort" path if the end could not be reached *(Note: This can take up to 40 seconds for each attempt and seriously slow down your terminal)*:
```
false; while [ $? -ne 0 ]; do time ./gravedigger.py 200 200 --printseed --complexity 15 --mode dungeon --start 0,0 --end 199,199 | ./boobytraps.py -v2; done
```
