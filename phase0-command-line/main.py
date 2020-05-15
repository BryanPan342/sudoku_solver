import argparse
import numpy as np
import time
import sys
from utils import *

##### SUDOKU CONSTRAINTS #####
def reduce_grid(values, index, val):
    if val not in values[index]:
        return values
    values[index] = values[index].replace(val,'')
    if len(values[index]) == 0:
        return False
    elif len(values[index]) == 1:
        singular_val = values[index]
        if not all(reduce_grid(values, i, singular_val) for i in c_index_dict[index]):
            return False
    for arr in index_dict[index]:
        other_places = [i for i in arr if val in values[i]]
        if len(other_places) == 0:
            return False
        elif len(other_places) == 1:
            if not test(values, other_places[0], val):
                return False
    return values

def test(values, index, val):
    other_values = values[index].replace(val, '')
    if all(reduce_grid(values, index, v) for v in other_values):
        return values
    else:
        return False

##### TRANSFORM GRID #####
def obtain_values(grid):
    vals = [v for v in grid if v in numbers or '0.']
    return dict(zip(super_matrix, vals))

def transform_grid(grid):
    values = dict((index, numbers) for index in super_matrix)
    for index, val in obtain_values(grid).items():
        if val in numbers and not test(values, index, val):
            return False
    return values
        
##### BACKTRACE ALGORITHM #####
def backtrace(p_values):
    if p_values is False:
        return False
    if all(len(p_values[index]) == 1 for index in super_matrix):
        return p_values
    l, index = min((len(p_values[index]), index) for index in super_matrix if len(p_values[index]) > 1)
    return ret_one(backtrace(test(p_values.copy(), index, val)) for val in p_values[index])

##### AUXILIARY FUNCTION #####
def ret_one(values):
    for v in values:
        if v:
            return v
    return False

##### SOLVE FUNCTION #####
def solve(grid, t_threshold=0.0):
    start_t = time.clock()
    values = backtrace(transform_grid(grid))
    delta_t = time.clock() - start_t
    if t_threshold is not None and delta_t > t_threshold:
        print("PUZZLE:", file = outfile)
        show(obtain_values(grid), outfile)
        print("\nSOLUTION:", file = outfile)
        if values:
            show(values, outfile)
    print('\n============================================\n', file = outfile)
    values = not not values
    return (delta_t, values)

def solve_wrapper(grids, t_threshold=0.0):
    times, results = zip(*[solve(grid) for grid in grids])
    num = len(times)
    if num > 1:
        print("Solved %d of %d puzzles (avg %.5f secs, max %.5f secs)." % (
            sum(results), num, sum(times)/num, max(times)))
    if num == 1:
        print("Puzzle solved in %.5f secs" % (times[0]))

##### ARGUMENT PARSING #####
parser = argparse.ArgumentParser(description='Sudoku Solver')
parser.add_argument("--puzzle", "-p", type=str, help='Puzzle in \'.123456789\' format')
parser.add_argument("--file", "-f", type=str, help='Input File')
parser.add_argument("--output", "-o", type=str, help='Output File')
args = parser.parse_args()

##### MAIN #####
if __name__ == "__main__":
    if not args.file and not args.puzzle:
        print("Please use --puzzle or --file to insert a puzzle(s)\n")
        sys.exit()
    if args.output:
        outfile = open(args.output, 'w')
    elif args.file:
        outfile = open('answer.txt', 'w')
    else:
        outfile = sys.stdout
    if args.puzzle:
        grids = [args.puzzle]
        solve_wrapper(grids, None)
    if args.file:
        f = open(args.file, 'r')
        grids = f.read().strip().split('\n')
        f.close()
        solve_wrapper(grids, None)
    if args.output:
        outfile.close()