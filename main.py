import argparse
import numpy as np
import sys
from copy import copy, deepcopy

parser = argparse.ArgumentParser(description='Sudoku Solver')
args = parser.parse_args()

ans = []

def print_sudoku(grid):
    for r in grid:
        print(r)

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
        

def backtrace_solution(grid):
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
    ans.append(m)

if __name__ == "__main__":
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
    print("Solution is as follows:")
    print_sudoku(ans[0])
        

