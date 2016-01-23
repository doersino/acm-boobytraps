# acm-boobytraps

My Python 2.7 solution of the ACM Programming Contest problem ["Booby Traps"](https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&category=258&page=show_problem&problem=1649), created as part of my assignment for the ["Selected Fun Problems of the ACM Programming Contest" proseminar](http://db.inf.uni-tuebingen.de/teaching/SelectedFunProblemsoftheACMProgrammingContest-Proseminar-WS2015-2016.html) at Uni Tübingen during the 2015 fall semester, including a map generator and a LaTeX beamer slide and map visualization generator.

![screenshot](https://github.com/doersino/acm-boobytraps/raw/master/screenshot.png)


## Table of Contents

Books tend to have one, so why shouldn't software?


### Problem Statement and Solution

* `boobytraps.pdf` is the problem statement.
* `boobytraps.py` contains the code solving the problem.


### Input and Output

* `gravedigger.py` is a simple map generator I've written for testing the performance of `boobytraps.py` on large maps. Run it with the `-h` flag to find out how to use it.
* `sampleinput.txt` contains the sample input given on the problem statement.
* `sampleinput[0-9]+.txt` contain other interesting sample inputs.
* `sampleoutput.txt` contains the sample output given on the problem statement.


### LaTeX Code Generation

* `boobytraps-latex.py` generates code for LaTeX Beamer slides stepping through the algorithm implemented in `boobytraps.py` based on any valid input, or outputs the code for a Ti*k*Z representation of a map.
* `boobytraps-latex-preamble.tex` contains the package imports and macros required for compiling LaTeX code generated by `boobytraps-latex.py`.
* `boobytraps-latex-output-sampleinput9.tex` contains the output of `cat sampleinput9.txt | ./boobytraps-latex.py slides`.
* `boobytraps-latex-example.tex` combines `boobytraps-latex-preamble.tex` and `boobytraps-latex-output-sampleinput9.tex` into a valid LaTeX document.
* `boobytraps-latex-example.pdf` is the example output after compiling `boobytraps-latex-example.tex`.

### Other files

* `README.md` is the file you're looking at right now.
* `repeatoffender.sh` is a tool for benchmarking `boobytraps.py`.
* `screenshot.png` shows the shortest path finder in action on the sample input.
* `screenshot2.png` shows the map generator and shortest path finder in action.
* `tombraider.sh` is a short shell script for semi-automated testing of my solution.


## Example Usage

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
Using the `-v2` flag instead will, in addition, highlight visited cells and the "best effort" path (if none from start to end is found) in the map.


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

Randomly generate 40x20 maps (with a high map complexity) and print the random seed used for map generation until one with a shortest path from start to end is found, then highlight this path in the map (along with all visited cells), also output the time taken for each map generation/path finding attempt *(see screenshot)*:
```
false; while [ $? -ne 0 ]; do time ./gravedigger.py 40 20 --start 0,0 --end 39,19 --complexity 15 --printseed | ./boobytraps.py -v; done
```

![screenshot3](https://github.com/doersino/acm-boobytraps/raw/master/screenshot3.png)

Randomly generate 40x20 maps (using the "dungeon" mode) until one with a shortest path from start to end is found, then highlight this path in the map, also output the time taken for each map generation/path finding attempt:
```
false; while [ $? -ne 0 ]; do time ./gravedigger.py 40 20 --mode dungeon | ./boobytraps.py -v; done
```

Randomly generate giant 202x51 maps (using the "dungeon" mode and higher-than normal map complexity) and print the random seed used for map generation until one with a shortest path from the upper left cell to the lower right cell is found, then highlight this path in the map, also output the time taken for each map generation/path finding attempt *(see screenshot)*:
```
false; while [ $? -ne 0 ]; do time ./gravedigger.py 202 51 --printseed --complexity 15 --mode dungeon --start 0,0 --end 201,50 | ./boobytraps.py -v; done
```

![screenshot2](https://github.com/doersino/acm-boobytraps/raw/master/screenshot2.png)

As above, but with the maximum map size permitted by the problem statement and additional highlighting of visited cells as well as the "best effort" path if the end could not be reached *(Note: This can take up to 40 seconds for each attempt and seriously slow down your terminal)*:
```
false; while [ $? -ne 0 ]; do time ./gravedigger.py 200 200 --printseed --complexity 15 --mode dungeon --start 0,0 --end 199,199 | ./boobytraps.py -v2; done
```


### `boobytraps-latex.py`
Generate code for a Ti*k*Z representation of the `sampleinput.txt`, including the shortest path:
```
cat sampleinput.txt | ./boobytraps-latex.py map
```

In the previous example, also draw the internal graph representation of the map:
```
cat sampleinput.txt | ./boobytraps-latex.py map --drawgraph
```

And draw everything at a third of the original size:
```
cat sampleinput.txt | ./boobytraps-latex.py map --drawgraph --scale 0.33
```

Generate code for LaTeX Beamer slides stepping through the shortest path finder running on `sampleinput9.txt` and write to `boobytraps-latex-output-sampleinput9.tex`:
```
cat sampleinput9.txt | ./boobytraps-latex.py slides > boobytraps-latex-output-sampleinput9.tex
```

In the previous example, set slide title and subtitle (with output of the step number instead of `{}`), also draw the graph and write to standard output:
```
cat sampleinput9.txt | ./boobytraps-latex.py slides --title "Beispiel" --subtitle "Schritt {}: TODO" --drawgraph
```


### `repeatoffender.sh`

Run `boobytraps.py` 100 times for each map side length from 1 to 200 and write the results to `repeatoffender.csv`:
```
./repeatoffender.sh -n 100
```

Run `boobytraps.py` only 5 times for each map side length from 1 to 200 and write the results to `test.csv` (the remaining options are passed to `gravedigger.py` for random map generation):
```
./repeatoffender.sh -n 5 -o test.csv --complexity 12 --mode dungeon
```

Run `boobytraps.py` 300 times for each map side length from 1 to 200 and write the results to `repeatoffender-example.csv` (the remaining option is passed to `gravedigger.py` for random map generation):
```
./repeatoffender.sh -n 300 -o repeatoffender-example.csv --complexity 12
```


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
