import argparse
import numpy as np
import time
import sys

##### UNIVERSAL UTILITY #####

#####   DATA STRUCTURES FOR   #####
##### CONSTRAINED BACKTRACING #####
# Function to take cross product of two vectors
def combine(X, Y):
    return [x+y for x in X for y in Y]

### SET UP ###
numbers         = '123456789'                               # Columns Values          A1 A2 A3 A4 A5..  
chars           = 'ABCDEFGHI'                               # Rows Values             B1 B2 B3 B4 B5..
super_matrix    = combine(chars, numbers)                   # A1 - I9 Matrix          C1 C2 C3 C4 C5..        
master_rows     = [combine(chars, n) for n in numbers]      # Array of all rows       [[A1-9], ..., [I1-9]]
master_cols     = [combine(c, numbers) for c in chars]      # Array of all cols       [[A-I1], ..., [A-I9]]
master_squares  = [combine(cs, ns) for cs in ('ABC', 'DEF','GHI') for ns in ('123', '456', '789')]

### REAL STUFF ###
# master_list   - holds combination of all rows, cols and squares
master_list     = (master_rows + master_cols + master_squares)

# index_dict    - dictionary correlating every square to their impacted squares
index_dict      = dict((index, [s for s in master_list if index in s]) for index in super_matrix)

# c_index_dict  - cleaned up dictionary removing self and duplicates
c_index_dict    = dict((index, set(sum(index_dict[index],[])) - set([index])) for index in super_matrix)

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
    grid = ''.join(map(str, grid))
    start_t = time.clock()
    values = backtrace(transform_grid(grid))
    delta_t = time.clock() - start_t
    
    ans = [int(values[c]) for c in super_matrix]
    return (delta_t, ans)