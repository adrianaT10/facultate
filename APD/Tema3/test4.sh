#!/bin/bash

time mpirun -np 16 sudoku top4 4/4-1.txt out4-1 >output4
diff out4-1 4/4-1-solution.txt -w
