import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        for x in range(self.life.cols + 2):
            if x == 0 or x == self.life.cols + 1:
                screen.addstr(0, x, "+")
            else:
                screen.addstr(0, x, "-")
        for x in range(1, self.life.rows + 1):
            screen.addstr(x, 0, "|")
            screen.addstr(x, self.life.cols + 1, "|")
        for x in range(self.life.cols + 2):
            if x == 0 or x == self.life.cols + 1:
                screen.addstr(self.life.rows + 1, x, "+")
            else:
                screen.addstr(self.life.rows + 1, x, "-")

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for x in range(1, self.rows - 1):
            for y in range(1, self.cols - 1):
                if self.life.curr_generation[x][y] == 1:
                    screen.addstr(x + 1, y + 1, "*")
                else:
                    screen.addstr(x + 1, y + 1, " ")

    def run(self) -> None:
        screen = curses.initscr()
        self.draw_borders(screen)
        self.draw_grid(screen)
        screen.refresh()
        time.sleep(1)
        while not self.life.is_max_generations_exceed and self.life.is_changing:
            self.life.step()
            self.draw_grid(screen)
            screen.refresh()
            time.sleep(1)
        screen.clear()
        curses.endwin()
