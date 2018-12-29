#!/bin/bash
for i in 1 2 3 4; do
	time mpirun -np 9 sudoku top3 3/3-$i.txt out3-$i >output3-$i
done
for i  in 1 2 3 4; do
	diff out3-$i 3/3-$i-solution.txt -w
done
