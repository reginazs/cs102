import curses
import curses.ascii
from time import sleep

import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)

        self.cell_size = cell_size
        self.speed = speed
        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border()

    def draw_lines(self) -> None:
        for i in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (i, 0), (i, self.height))
        for j in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, j), (self.width, j))

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addch(i + 1, j + 1, "*")
                else:
                    screen.addch(i + 1, j + 1, " ")

    def run(self) -> None:
        screen = curses.initscr()
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.full(pygame.Color("white"))

        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (cell_y, cell_x) = pygame.mouse.get_pos()
                    self.change_state((cell_x, cell_y))
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()
                    clock.tick(self.speed)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = not pause
            if not pause:
                self.life.step()

            self.draw_grid()
            self.draw_lines

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()
        curses.endwin()


def main():
    game = GameOfLife(size=(48, 64))
    app = GUI(game)
    app.run()


if __name__ == "__main__":
    main()
