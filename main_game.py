from tkinter import Tk, Canvas, Button
from random import randint
class GameOfLife:
    """GameOfLife is a Tkinter application displaying a canvas on which you can
    put cells to life or death, and run in which case the rules of GOL will apply
    and you will see how your simulation goes.
    """
    def __init__(self):
        self.window=Tk()
        self.width=100
        self.height=100
        self.pause=True
        self.window.title("Game of Life | paused | 10")
        self.cell_size=5
        self.delay=10
        # Set up the size of the canvas.
        self.window.geometry("1000x500")

        # Create the canvas widget and add it to the Tkinter application window.
        self.canvas = Canvas(self.window, width=self.width*self.cell_size,
                             height=self.height*self.cell_size, bg='white')
        self.canvas.grid(row=0, column=0)

        # Set up an empty game grid.
        self.grid = [[0 for column in range(self.width)] for row in range(self.height)]

        # Set a click event on the canvas.
        self.window.bind('<Button-1>',      self.canvas_click_alive)
        self.window.bind('<Button1-Motion>',self.canvas_click_alive)
        self.window.bind("<Return>",        self.pause_game)
        self.window.bind("<Button-3>",      self.canvas_click_dead)
        self.window.bind("<Button3-Motion>",self.canvas_click_dead)
        self.window.bind("<BackSpace>",     self.reset_game)
        self.window.bind("[",               self.slow_game)
        self.window.bind("]",               self.fast_game)
        self.b_randompat=Button(self.window, text="Pattern aléatoire",
                                font="Arial 12", command=self.create_random_pattern)
        self.b_randompat.grid(row=1, column=0)

        # Start the timer.
        self.window.after(10, self.update_board)
        self.window.mainloop()

    def draw_board(self):
        for row in range(self.height):
            for column in range(self.width):
                pos_y=row*self.cell_size
                pos_x=column*self.cell_size
                if self.grid[row][column]==1:
                    self.canvas.create_rectangle(pos_y, pos_x,
                                                 pos_y+self.cell_size,
                                                 pos_x+self.cell_size,
                                                 fill='black', outline='black')

    def run_game(self):
        new_board= [[0 for column in range(self.width)] for row in range(self.height)]
        if not self.pause:
            for row in range(self.height):
                for column in range(self.width):
                    nb_neighbors=self.number_of_neighbors(row, column)
                    if self.grid[row][column] == 1:
                        if nb_neighbors in (2, 3):
                            new_board[row][column]=0
                        if (nb_neighbors==2 or nb_neighbors==3):
                            new_board[row][column]=1
                    else:
                        if nb_neighbors==3:
                            new_board[row][column]=1
            return new_board
        return self.grid

    def number_of_neighbors(self, row, column):
        neighbors=0
        xrange = [column-1, column, column+1]
        yrange = [row-1, row, row+1]
        for place in range(3):
            if xrange[place]<0:
                xrange[place]=xrange[place]+self.width
            if xrange[place]>(self.width-1):
                xrange[place]=xrange[place]-self.width
            if yrange[place]<0:
                yrange[place]=yrange[place]+self.height
            if yrange[place]>(self.height-1):
                yrange[place]=yrange[place]-self.height
        for column_1 in xrange:
            for row_1 in yrange:
                if column_1 == column and row_1 == row:
                    # Don't count this cell.
                    continue
                try:
                    if self.grid[row_1][column_1] == 1:
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
        self.window.after(self.delay, self.update_board)

    def canvas_click_alive(self, event):
        if self.pause:
            # Work out where the mouse is in relation to the grid.
            gridx = int(event.y/self.cell_size)
            gridy = int(event.x/self.cell_size)
            self.grid[gridy][gridx] = 1
            self.draw_board()

    def canvas_click_dead(self, event):
        if self.pause:
            # Work out where the mouse is in relation to the grid.
            gridx = int(event.y/self.cell_size)
            gridy = int(event.x/self.cell_size)
            self.grid[gridy][gridx] = 0
            self.draw_board()
    def pause_game(self, event=None):
        self.pause=not self.pause
        if not self.pause:
            self.run_game()
            self.window.wm_title(f"Game of Life | running | {self.delay}")
        else:
            self.window.wm_title(f"Game of Life | paused | {self.delay}")

    def reset_game(self, event=None):
        self.canvas.delete('all')
        if not self.pause:
            self.pause_game()
        self.grid = [[0 for column in range(self.width)] for row in range(self.height)]
        self.draw_board()

    def slow_game(self, event=None):
        if self.delay>1:
            self.delay-=1
            self.window.wm_title(f"Game of Life | running | {self.delay}")

    def fast_game(self, event=None):
        if self.delay<100:
            self.delay+=1
            self.window.wm_title(f"Game of Life | running | {self.delay}")

    def create_random_pattern(self, event=None):
        self.grid= [[1 if (randint(1, self.cell_size)==self.cell_size)
                     else 0 for column in range(self.width)]
                    for row in range(self.height)]
        if not self.pause:
            self.pause_game()
        self.draw_board()
GameOfLife()