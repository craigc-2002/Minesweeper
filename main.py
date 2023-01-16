"""
Minesweeper clone

Craig Cochrane, 2023
"""

import pygame

import minesweeper

"""
TO DO:

"""

# ---Setup---
pygame.init()  # Initialise pygame


class Minesweeper:
    """
    Class to handle the game logic of the minesweeper game
    """

    def __init__(self):
        # Set the dimensions of the window
        self.window_width = 1280
        self.window_height = 720

        # Set up the window to the required dimensions, name it and create a clock object
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()

        self.grid_size = (500, 500)
        self.game_grid = minesweeper.Grid(self, (10, 10), self.grid_size)
        self.grid_position = (390, 130)
        # print(self.game_grid)

        self.font = pygame.font.SysFont('consolas', 30)
        self.title_font = pygame.font.SysFont('consolas', 100)
        self.subtitle_font = pygame.font.SysFont('consolas', 50)

        self.colours = {"flagged_square": (255, 0, 0),
                        "zero_square": (2, 125, 35),
                        "square_text": (12, 0, 105),
                        "unclicked_square": (2, 207, 57),
                        "square_border": (255, 255, 255),
                        "text": (0, 0, 0),
                        "text_shadow": (196, 196, 196),
                        "clicked_mine": (0, 0, 0),
                        "background": (255, 253, 237)}

        self.game_loop()

    def game_loop(self):
        # ---Main Game Loop---
        while True:
            # Check event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_click(event)

            self.screen.fill(self.colours["background"])

            title = self.title_font.render("MINESWEEPER", True, self.colours["text"])
            title_shadow = self.title_font.render("MINESWEEPER", True, self.colours["text_shadow"])
            title_pos = ((self.window_width / 2) - (title.get_width() / 2), 10)
            shadow_offset = 5
            self.screen.blit(title_shadow, (title_pos[0] + shadow_offset, title_pos[1] + shadow_offset))
            self.screen.blit(title, title_pos)

            # Display screen updates here
            grid = self.game_grid.draw()
            self.screen.blit(grid, self.grid_position)

            flag_count = self.font.render(f"Flags: {self.game_grid.num_flags}/{self.game_grid.num_mines}",
                                          True, self.colours["text"])
            self.screen.blit(flag_count, (900, 360))

            pygame.display.flip()  # Display the screen updates
            self.clock.tick(60)  # Advance the clock (limited to 60FPS)

    def win(self):
        self.game_over(loss=False)

    def game_over(self, loss=True):
        while True:
            # Check event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.restart()

            self.screen.fill((255, 253, 237))

            title = self.title_font.render("MINESWEEPER", True, self.colours["text"])
            title_shadow = self.title_font.render("MINESWEEPER", True, self.colours["text_shadow"])
            title_pos = ((self.window_width / 2) - (title.get_width() / 2), 10)
            shadow_offset = 5
            self.screen.blit(title_shadow, (title_pos[0] + shadow_offset, title_pos[1] + shadow_offset))
            self.screen.blit(title, title_pos)

            subtitle = self.subtitle_font.render("CLICK TO REPLAY", True, self.colours["text"])
            self.screen.blit(subtitle, ((self.window_width / 2) - (subtitle.get_width() / 2), 650))

            grid = self.game_grid.draw()
            self.screen.blit(grid, self.grid_position)

            if loss:
                ending_message = "GAME OVER"
            else:
                ending_message = "YOU WON"

            end_message = self.title_font.render(ending_message, True, (255, 0, 0))
            self.screen.blit(end_message, ((self.window_width / 2) - (end_message.get_width() / 2),
                                           (self.window_height / 2) - (end_message.get_height() / 2)))

            pygame.display.flip()  # Display the screen updates
            self.clock.tick(60)  # Advance the clock (limited to 60FPS)

    def restart(self):
        self.game_grid = minesweeper.Grid(self, (10, 10), self.grid_size)
        self.game_loop()

    def mouse_click(self, event):
        click_location = event.pos
        if (self.grid_position[0] + self.grid_size[0]) > click_location[0] > self.grid_position[0] and \
                (self.grid_position[1] + self.grid_size[1]) > click_location[1] > self.grid_position[1]:
            location_on_grid = (click_location[0] - self.grid_position[0],
                                click_location[1] - self.grid_position[1])
            self.game_grid.click(location_on_grid, event.button)

    def mine_clicked(self):
        self.game_grid.show_mines()
        self.game_over()


if __name__ == "__main__":
    Minesweeper()
