import pygame
import random


class GridSquare:
    """
    Class to represent a single square on the minesweeper grid

    Contains the square's state, and methods to handle clicks on the square and drawing the square
    """
    def __init__(self, game, grid, grid_coords: tuple, size: tuple):
        self.game = game
        self.grid = grid
        self.grid_coords = grid_coords
        self.size = size

        self.clicked = False
        self.mine = False
        self.flag = False
        self.number = 0

        self.font = pygame.font.SysFont('consolas', 30)

    def set_mine(self):
        self.mine = True

    def numbers(self):
        self.number = self.grid.get_surrounding_mines(self.grid_coords)

    def show(self):
        self.clicked = True

    def click(self, button=1):
        if not self.clicked:
            if button == 3:
                if self.flag:
                    self.flag = False
                    self.grid.remove_flag()
                else:
                    self.flag = True
                    self.grid.add_flag()
            elif button == 1 and not self.flag:
                self.clicked = True

                if self.mine:
                    self.game.mine_clicked()
                elif self.number == 0:
                    self.grid.show_neighbours(self.grid_coords)
            self.grid.check_win()

    def draw(self, surf):
        display_coords = ((self.grid_coords[0] * self.size[0]),
                          (self.grid_coords[1] * self.size[1]))

        colour = self.game.colours["unclicked_square"]
        if self.number == 0 and self.clicked:
            colour = self.game.colours["zero_square"]
        if self.flag and not self.clicked:
            colour = self.game.colours["flagged_square"]
        if self.mine and self.clicked:
            colour = self.game.colours["clicked_mine"]

        pygame.draw.rect(surf, colour, (display_coords, self.size))
        pygame.draw.rect(surf, self.game.colours["square_border"], (display_coords, self.size), width=1)

        if self.clicked:
            if self.mine is not True and self.number != 0:
                num = self.font.render(str(self.number), True, self.game.colours["square_text"])
                text_pos = (display_coords[0] + (self.size[0] / 2) - (num.get_width() / 2),
                            display_coords[1] + (self.size[1] / 2) - (num.get_height() / 2))
                surf.blit(num, text_pos)

    def __repr__(self):
        return f"[{self.number}]" if self.mine is False else "[M]"


class Grid:
    """
    Class to represent the whole game grid

    Contains each of the grid squares and coordinates mouse clicks and displaying the grid
    """
    def __init__(self, game, grid_dims: tuple, size: tuple, num_mines=10):
        self.game = game
        self.grid_dims = grid_dims
        self.size = size
        self.num_mines = num_mines
        self.num_flags = 0

        self.squares = []
        self.square_size = (self.size[0] / self.grid_dims[0], self.size[1] / self.grid_dims[1])

        self.generate_grid()

    def generate_grid(self):
        for x in range(self.grid_dims[0]):
            col = []
            for y in range(self.grid_dims[1]):
                col.append(GridSquare(self.game, self, (x, y), self.square_size))

            self.squares.append(col)

        self.assign_mines()

        for row in self.squares:
            for square in row:
                square.numbers()

    def assign_mines(self):
        mines_assigned = 0
        while mines_assigned < self.num_mines:
            random_coords = (random.randint(0, self.grid_dims[0]-1), random.randint(0, self.grid_dims[1]-1))

            new_mine = self.squares[random_coords[0]][random_coords[1]]
            if new_mine.mine is False:
                new_mine.set_mine()
                mines_assigned += 1

    def get_surrounding_mines(self, grid_coords):
        num_surrounding_mines = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                target_square = (grid_coords[0]+x, grid_coords[1]+y)
                if (target_square[0] >= 0 and target_square[1] >= 0) and \
                        (target_square[0] < len(self.squares) and target_square[1] < len(self.squares[0])):
                    if self.squares[grid_coords[0]+x][grid_coords[1]+y].mine:
                        num_surrounding_mines += 1

        return num_surrounding_mines

    def draw(self):
        grid_surf = pygame.Surface(self.size)

        for row in self.squares:
            for square in row:
                square.draw(grid_surf)

        return grid_surf

    def click(self, location: tuple, button):
        square_clicked_x = int(location[0] // self.square_size[0])
        square_clicked_y = int(location[1] // self.square_size[1])
        self.squares[square_clicked_x][square_clicked_y].click(button)

    def show_mines(self):
        for row in self.squares:
            for square in row:
                if square.mine:
                    square.show()

    def show_neighbours(self, grid_coords):
        for x in range(-1, 2):
            for y in range(-1, 2):
                target_square_pos = (grid_coords[0]+x, grid_coords[1]+y)
                if (target_square_pos[0] >= 0 and target_square_pos[1] >= 0) and \
                        (target_square_pos[0] < len(self.squares) and target_square_pos[1] < len(self.squares[0])):
                    target_square = self.squares[target_square_pos[0]][target_square_pos[1]]
                    target_square.click()

    def check_win(self):
        win = True
        for col in self.squares:
            for square in col:
                if not (square.clicked or square.flag):
                    win = False
        if win:
            self.game.win()

    def add_flag(self):
        self.num_flags += 1

    def remove_flag(self):
        self.num_flags -= 1

    def __repr__(self):
        grid_string = ""
        for y in range(len(self.squares[0])):
            row_string = ""
            for x in range(len(self.squares)):
                row_string += "{} ".format(self.squares[x][y])
            row_string += "\n"
            grid_string += row_string

        return grid_string
