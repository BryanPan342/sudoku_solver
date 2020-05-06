from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

MARGINS = 25
SQUARE = 50
DIMENSION = 9*SQUARE + 2*MARGINS

class SudokuBoard(object):
    def __init__(self, infile=0):
        self.infile = infile
        self.init_puzzle = '0'*81
    def solve():
        self.infile = 1

class SudokuUI(Frame):
    def __init__(self, root, board):
        self.board = board
        self.root= root
        Frame.__init__(self, root)
        # self.row = 0      only necessary if we want a cursor or square highlighted
        # self.col = 0
        self.__init_interface()
    
    def __init_interface(self):
        self.root.title = "Sudoku Board"
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=DIMENSION, height=DIMENSION)
        self.canvas.pack(fill=BOTH, side=TOP)
        solve_button = Button(self, text="Solve", command=self.board.solve)
        solve_button.pack(fill=BOTH, side=BOTTOM)
        
        self.__draw_grid()
        self.__draw_board()

        self.canvas.bind("<Button-1>", self.__click)
        self.canvas.bind("<Key>", self.__key_press)
    
    def __click(self, event):
        print("click")

    def __key_press(self, event):
        print("keys")
    
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
            color = "black"

            x = MARGINS + (j * SQUARE) + (SQUARE / 2)
            y = MARGINS + (i * SQUARE) + (SQUARE / 2)
            self.canvas.create_text(x, y, text=init, tags="newbies", fill=color)

if __name__ == '__main__':
    board = SudokuBoard()
    root = Tk()
    SudokuUI(root, board)
    root.mainloop()
