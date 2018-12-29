#!/bin/bash
for i in 1 2 3; do
	time mpirun -np 4 sudoku top2 2/2-$i.txt out2-$i >output2-$i
done
for i  in 1 2 3; do
	diff out2-$i 2/2-$i-solution.txt -w
done
