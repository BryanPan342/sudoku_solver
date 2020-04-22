import argparse
import numpy as np
from copy import copy, deepcopy
import time

##### UNIVERSAL UTILITY #####
def combine(X, Y):
    return [x+y for x in X for y in Y]

def show(values):
    max_width = 1+max(len(values[index]) for index in super_matrix)
    divider = '+'.join(['-'*max_width*3]*3)
    for c in chars:
        print(''.join(values[c+n].center(max_width)+('|' if n in '36' else '') for n in numbers))
        if c in 'CF':
            print(divider)

numbers         = '123456789'
chars           = 'ABCDEFGHI'
super_matrix    = combine(chars, numbers)
master_rows     = [combine(chars, n) for n in numbers]
master_cols     = [combine(c, numbers) for c in chars]
master_squares  = [combine(cs, ns) for cs in ('ABC', 'DEF', 'GHI') for ns in ('123', '456', '789')]
master_list     = (master_rows + master_cols + master_squares)
index_dict      = dict((index, [s for s in master_list if index in s]) for index in super_matrix)
c_index_dict    = dict((index, set(sum(index_dict[index],[])) - set([index])) for index in super_matrix)

##### ARGUMENT PARSING #####
parser = argparse.ArgumentParser(description='Sudoku Solver')
parser.add_argument("--file", "-f", type=str, required=True, help='Input File')
args = parser.parse_args()

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
        print("PUZZLE:")
        show(obtain_values(grid))
        print("\nSOLUTION:")
        if values:
            show(values)
    print('\n============================================\n')
    values = not not values
    return (delta_t, values)

def solve_wrapper(grids, t_threshold=0.0):
    times, results = zip(*[solve(grid) for grid in grids])
    num = len(times)
    if num > 1:
        print("Solved %d of %d puzzles (avg %.5f secs, max %.5f secs)." % (
            sum(results), num, sum(times)/num, max(times)))

if __name__ == "__main__":
    f = open(args.file, 'r')
    grids = f.read().strip().split('\n')
    f.close()
    solve_wrapper(grids, None)
   