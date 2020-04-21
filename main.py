import argparse
import numpy as np
from copy import copy, deepcopy

##### UNIVERSAL DATA STRUCTURES #####
def combine(X, Y):
    return [x+y for x in X for y in Y]

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
args = parser.parse_args()

##### SUDOKU CONSTRAINTS #####
def reduce(values, index, val):
    if val not in values[index]:
        return values
    values[index] = values[index].replace(val,'')
    if len(values[index]) == 0:
        return False
    elif len(values[index]) == 1:
        singular_val = values[index]
        if not all(reduce(values, i, singular_val) for i in c_index_dict[index])
            return False
    for arr in index_dict[index]:
        other_places = [i for i in arr if val in values[index]]
        if len(other_places) == 0:
            return False
        elif len(other_places) == 1:
            if not test(values, other_places[0], val)
                return False
    return values

def test(values, index, val):
    other_values = values[index].replace(val, '')
    if all(reduce(values, index, v) for v in other_values):
        return values
    else
        return False

##### TRANSFORM GRID #####
def transform_grid(grid):
    p_values = dict((index, numbers) for index in super_matrix)


def isPossible(x, y, n, grid):
    grid_x = int(x/3)*3
    grid_y = int(y/3)*3
    if n in grid[y]:
        return False
    for i in range(9):
        if grid[i][x] == n:
            return False
    for j in range(3):
        for i in range(3):
            if grid[j+grid_y][i+grid_x] == n:
                return False
    return True
        

def backtrace(p_values):
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1,10):
                    if isPossible(x, y, n, grid):
                        grid[y].pop(x)
                        grid[y].insert(x, n)
                        backtrace_solution(grid)
                        grid[y].pop(x)
                        grid[y].insert(x, 0)
                return
    m = list(map(list, grid))
    print_sudoku(m)
    ans.append(m)
    return

def solve(grid):
    p_values = transform_grid(grid)
    return search(p_values)


if __name__ == "__main__":
    s = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
    matrix2 = []
    for i in range(len(s)):
        if i%9 == 0:
            matrix2.append([])
        temp = 0 if s[i] == "." else int(s[i]) 
        matrix2[int(i/9)].append(temp)
    matrix = [[2, 0, 7, 0, 0, 0, 0, 6, 8],
              [0, 9, 0, 6, 8, 7, 3, 0, 2],
              [8, 0, 0, 2, 5, 0, 1, 9, 0],
              [3, 1, 0, 0, 0, 9, 6, 0, 0],
              [0, 0, 0, 0, 6, 0, 7, 0, 4],
              [0, 7, 4, 0, 0, 8, 2, 1, 9],
              [0, 0, 0, 0, 9, 1, 4, 0, 0],
              [0, 3, 0, 0, 0, 0, 8, 5, 1],
              [7, 0, 0, 0, 4, 0, 0, 0, 6]]
    backtrace_solution(matrix)
