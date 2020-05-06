from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, RIGHT
import argparse
import numpy as np
import time
from solve import solve

MARGINS = 25
SQUARE = 50
DIMENSION = 9*SQUARE + 2*MARGINS

class SudokuBoard(object):
    def __init__(self, init_board):
        self.infile = init_board
        self.solved = False
    
    def init_board(self):
        self.init_puzzle = [0]*81
        if self.infile != None:
            for i in range(81):
                self.init_puzzle[i] = 0 if self.infile[i] == '.' else int(self.infile[i])
        self.puzzle = self.init_puzzle

    def solve(self):
        if not self.solved:
            self.init_puzzle = self.puzzle
            print(self.init_puzzle)
            time, solution = solve(self.puzzle, 0)
            self.puzzle = solution
            self.solved = True

class SudokuUI(Frame):
    def __init__(self, root, board):
        self.board = board
        self.root= root
        Frame.__init__(self, root)
        self.row = 0  
        self.col = 0
        self.__init_interface()
    
    def __init_interface(self):
        self.root.title("Sudoku Board")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=DIMENSION, height=DIMENSION)
        self.canvas.pack(fill=BOTH, side=TOP)

        # Button Controls
        solve_button = Button(self, text="Clear Game", command=self.__clear_game)
        solve_button.pack(fill=BOTH, side=RIGHT)
        solve_button = Button(self, text="Clear Board", command=self.__clear)
        solve_button.pack(fill=BOTH, side=RIGHT)
        solve_button = Button(self, text="Solve", command=self.__solve)
        solve_button.pack(fill=BOTH, side=RIGHT)
        
        self.canvas.bind("<Button-1>", self.__click)
        self.canvas.bind("<Key>", self.__key_press)
        
        self.__draw_grid()
        self.__draw_board()

    def __clear(self):
        self.board.init_board()
        self.board.solved = False
        self.__draw_board()

    def __clear_game(self):
        self.board.solved = False
        self.board.puzzle = [0] * 81
        self.__draw_board()

    def __solve(self):
        self.board.solve()
        self.__draw_board()
    
    def __click(self, event):
        x = event.x
        y = event.y

        if MARGINS < x < DIMENSION - MARGINS and MARGINS < y < DIMENSION - MARGINS:
            self.canvas.focus_set()
            row = int((y-MARGINS)/SQUARE)
            col = int((x-MARGINS)/SQUARE)
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            else:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1
        
        self.__draw_selector()

    def __key_press(self, event):
        c = event.char
        if self.row >= 0 and self.col >= 0 and c in '01234567889':
            self.board.puzzle[self.row * 9 + self.col] = int(c)
            self.row, self.col = -1, -1
            self.__draw_board()
            self.__draw_selector()
    
    def __draw_grid(self):
        for i in range(10):
            color = "black" if i%3 == 0 else "gray"

            hy1 = hy0 = vx1 = vx0 = MARGINS + i*SQUARE
            hx0 = vy0 = MARGINS
            hx1 = vy1 = DIMENSION - MARGINS

            # horizontal line
            self.canvas.create_line(hx0, hy0, hx1, hy1, fill=color)

            # vertical line
            self.canvas.create_line(vx0, vy0, vx1, vy1, fill=color)

    def __draw_board(self):
        self.canvas.delete("newbies")
        for index in range(81):
            i = index % 9
            j = int(index / 9)
            init = self.board.init_puzzle[index]
            ans = self.board.puzzle[index]
            if ans != 0:
                color = "black" if ans == init else "blue"

                x = MARGINS + (i * SQUARE) + (SQUARE / 2)
                y = MARGINS + (j * SQUARE) + (SQUARE / 2)
                self.canvas.create_text(x, y, text=ans, tags="newbies", fill=color)

    def __draw_selector(self):
        self.canvas.delete("select")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGINS + (self.col * SQUARE) + 1
            x1 = MARGINS + ((self.col + 1) * SQUARE) -1
            y0 = MARGINS + (self.row * SQUARE) + 1
            y1 = MARGINS + ((self.row + 1) * SQUARE) -1
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="select")

def parse_arguments():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--board", help="Sudoku Board", type=str)
    args = arg_parser.parse_args()
    return args.board if args.board and len(args.board) == 81 else None

if __name__ == '__main__':
    board = parse_arguments()
    board = SudokuBoard(board)
    board.init_board()

    root = Tk()
    SudokuUI(root, board)
    root.mainloop()
