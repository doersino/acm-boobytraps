# acm-boobytraps

My Python 2.x solution of the ACM Programming Contest problem ["Booby Traps"](https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&category=258&page=show_problem&problem=1649), created as part of my assignment for the ["Selected Fun Problems of the ACM Programming Contest" proseminar](http://db.inf.uni-tuebingen.de/teaching/SelectedFunProblemsoftheACMProgrammingContest-Proseminar-WS2015-2016.html) at Uni Tübingen during the 2015 fall semester.

![screenshot](https://github.com/doersino/acm-boobytraps/raw/master/screenshot.png)

## Table of Contents
Books have one, so why shouldn't software?

* `boobytraps.py` contains the code solving the problem.
* `gravedigger.py` is a simple map generator I wrote for testing the performance of `boobytraps.py` on large maps.
* `sampleinput.txt` contains the sample input with which to test the solution.
* `sampleoutput.txt` contains the sample output with which to test the solution.
* `screenshot.png` shows my solution in action.
* `tombraider.sh` is a short shell script for efficiently testing the solution.

## Example Usage

Test the shortest path finder on the sample input and output given with the problem statement:
```
./tombraider.sh -i sampleinput.txt -o sampleoutput.txt
```

Test the shortest path finder on another sample input, specifying the expected output directly:
```
./tombraider.sh -i sampleinput2.txt -o 2
```

Test the shortest path finder on a third sample input (on which it currently fails to find the shortest path):
```
./tombraider.sh -i sampleinput2.txt -o 2
```

Randomly generate a 15x15 map and find the shortest path from start to end:
```
python gravedigger.py 15 15 | python boobytraps.py
```

Randomly generate a 15x10 map (with a fixed seed, using the "dungeon" mode and with start and end in the top left and bottom right corners), find the shortest path from start to end and highlight the path in the map:
```
python gravedigger.py 15 10 --seed donghwa --mode dungeon --start 0,0 --end 14,9 | python boobytraps.py -v
```

Randomly generate 40x20 maps (using the "dungeon" mode) until one with a shortest path from start to end is found, then highlight this path in the map, also output the time taken for each map generation/path finding attempt:
```
false; while [ $? -ne 0 ]; do time python gravedigger.py 40 20 --mode dungeon | python boobytraps.py -v; done
```
