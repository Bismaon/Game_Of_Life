from tkinter import Tk, Canvas
import math
from random import randint
class GameOfLife:
    def __init__(self):
        self.window=Tk()
        self.window.title("Game of Life")
        self.window.resizable(False, False)
        self.width=90
        self.height=90
        self.pause=True
        self.cell_size=10
        # Set up the size of the canvas.
        self.window.geometry(str(self.width*self.cell_size) + "x" + str(self.height*self.cell_size))

        # Create the canvas widget and add it to the Tkinter application window.
        self.canvas = Canvas(self.window, width=self.width*self.cell_size, height=self.height*self.cell_size,  bg='white')
        self.canvas.pack()
        # Set up an empty game grid.
        self.grid = [[0 for x in range(self.height)] for x in range(self.width)]
        self.draw_board()
        # Set a click event on the canvas.
        self.window.bind('<Button-1>', self.canvas_click)
        self.window.bind('<Button1-Motion>', self.canvas_click)
        self.window.bind("<Return>", self.pause_game)
        # Start the timer.
        self.window.after(10, self.update_board)
        self.window.mainloop()

    def draw_board(self):
        for row in range(self.height):
            for column in range(self.width):
                pos_x=row*self.cell_size
                pos_y=column*self.cell_size
                if self.grid[row][column]==1:
                    self.canvas.create_rectangle(pos_x, pos_y, pos_x+self.cell_size,
                                                 pos_y+self.cell_size, fill='black', outline='black')

    def run_game(self):
        new_board= [[0 for x in range(self.height)] for x in range(self.width)]
        if not self.pause:
            for x in range(self.height):
                for y in range(self.width):
                    nb_neighbors=self.number_of_neighbors(x, y)
                    if self.grid[x][y] == 1:
                        if nb_neighbors<2 or nb_neighbors>3:
                            new_board[x][y]=0
                        if (nb_neighbors==2 or nb_neighbors==3):
                            new_board[x][y]=1
                    else:
                        if nb_neighbors==3:
                            new_board[x][y]=1
            return new_board
        else:
            return self.grid

    def number_of_neighbors(self, x, y):
        neighbors=0
        xrange = [x-1, x, x+1]
        yrange = [y-1, y, y+1]
        for place in range(3):
            if xrange[place]==-1:
                xrange[place]=self.width
            if xrange[place]>self.width:
                xrange[place]=0
            if yrange[place]==-1:
                yrange[place]=self.height
            if yrange[place]>self.height:
                yrange[place]=0
        for x1 in xrange:
            for y1 in yrange:
                if x1 == x and y1 == y:
                    # Don't count this cell.
                    continue
                try:
                    if self.grid[x1][y1] == 1:
                        neighbors += 1
                except IndexError:
                    continue
        return neighbors

    def update_board(self):
        # Clear the canvas.
        self.canvas.delete("all")
        # Run the next generation and update the game grid.
        self.grid = self.run_game()
        # Generate the game board with the current population.
        self.draw_board()
        # Set the next tick in the timer.
        self.window.after(10, self.update_board)

    def canvas_click(self, event):
        if self.pause:
            # Work out where the mouse is in relation to the grid.
            gridx = int(event.x/self.cell_size)
            gridy = int(event.y/self.cell_size)
            # Make that cell alive.
            if self.grid[gridx][gridy] == 1:
                self.grid[gridx][gridy] = 0
            else:
                self.grid[gridx][gridy] = 1

    def pause_game(self, event):
        self.pause=not self.pause
        if not self.pause:
            self.run_game()
GameOfLife()