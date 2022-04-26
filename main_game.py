from tkinter import Tk, Canvas, Button, Label
from random import randint
class GameOfLife:
    """
    The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells,
    each of which is in one of two possible states, live or dead (or populated and unpopulated, respectively).
    Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically,
    or diagonally adjacent.
    """
    def __init__(self):
        self.window=Tk()
        self.width=120
        self.height=120
        self.pause=True
        self.window.title("Game of Life | paused | 10")
        self.cell_size=5
        self.delay=10
        self.generation=0
        for i in range(10):
            self.window.grid_rowconfigure(i,weight=1)
            self.window.grid_columnconfigure(i,weight=1)
        # Set up the size of the canvas.
        #self.window.geometry("1000x500")

        # Create the canvas widget and add it to the Tkinter application window.
        self.canvas = Canvas(self.window, width=self.width*self.cell_size,
                             height=self.height*self.cell_size, bg='white',
                             highlightthickness=1, highlightbackground="black")
        self.canvas.grid(row=0, column=5)

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
        self.b_randompat.grid(row=0, column=6)
        self.l_generation=Label(self.window, font="Arial 12",text=f"Génération: {self.generation}")
        self.l_generation.grid(row=1, column=5)
        # Start the timer.
        self.window.after(10, self.update_board)
        self.window.mainloop()

    def draw_board(self):
        """create all the cells on the canvas
        """
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
        """checks the whole grid to see if a cell should die or be alive

        Returns:
            list: the grid of the cells indicating their state (alive or dead)
        """
        new_board= [[0 for column in range(self.width)] for row in range(self.height)]
        if not self.pause:
            for row in range(self.height):
                for column in range(self.width):
                    nb_neighbors=self.number_of_neighbors(row, column)
                    if self.grid[row][column] == 1:
                        if nb_neighbors in (2, 3):
                            new_board[row][column]=0
                        if nb_neighbors in (2, 3):
                            new_board[row][column]=1
                    else:
                        if nb_neighbors==3:
                            new_board[row][column]=1
            return new_board
        return self.grid

    def number_of_neighbors(self, row, column):
        """counts the number of neighbors of one given cell

        Args:
            row (int): y axis of the grid
            column (int): x axis of the grid

        Returns:
            _type_: _description_
        """
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
                elif self.grid[row_1][column_1] == 1:
                    neighbors += 1
        return neighbors

    def update_board(self):
        """Updates the canvas periodically every self.delay miliseconds
        """
        # Clear the canvas.
        self.canvas.delete("all")
        # Run the next generation and update the game grid.
        self.grid = self.run_game()
        # Generate the game board with the current population.
        self.draw_board()

        if not self.pause:
            self.generation+=1
            self.window.wm_title(f"Game of Life | running | {self.delay}")
            self.l_generation['text']=f"Génération: {self.generation}"
        # Set the next tick in the timer.
        self.window.after(self.delay, self.update_board)

    def canvas_click_alive(self, event):
        """adds an alive cell to the canvas where the mouse clicks.

        Args:
            event (right mouse click)
        """
        if self.pause:
            # Work out where the mouse is in relation to the grid.
            gridx = int(event.y/self.cell_size)
            gridy = int(event.x/self.cell_size)
            if gridx>self.width-1: #checking if it is within the canvas x axis bound
                gridx-=self.width
            if gridy>self.height-1: #checking if it is within the canvas y axis bound
                gridy-=self.height
            self.grid[gridy][gridx] = 1
            self.draw_board()

    def canvas_click_dead(self, event):
        """kills a cell to the canvas where the mouse clicks.

        Args:
            event (left mouse click)
        """
        if self.pause:
            # Work out where the mouse is in relation to the grid.
            gridx = int(event.y/self.cell_size)
            gridy = int(event.x/self.cell_size)
            if gridx>self.width-1: #checking if it is within the canvas x axis bound
                gridx-=self.width
            if gridy>self.height-1: #checking if it is within the canvas y axis bound
                gridy-=self.height
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
        self.window.wm_title(f"Game of Life | paused | {self.delay}")
        self.generation=0
        self.l_generation['text']=f"Génération: {self.generation}"

    def slow_game(self, event=None):
        if self.delay>6:
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


def main():
    GameOfLife()

if __name__ == '__main__':
    main()