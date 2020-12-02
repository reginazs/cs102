import curses
import curses.ascii
import pathlib
from time import sleep

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife, save_path: pathlib.Path) -> None:
        super().__init__(life)
        self.save_path = save_path

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border()

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        tab = self.cell_size - 1
        for x in range(self.cell_width):
            for y in range(self.cell_height):
                if self.grid[y][x] != 0:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (
                            (self.cell_size * x + 1),
                            (self.cell_size * y + 1),
                            tab,
                            tab,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (
                            (self.cell_size * x + 1),
                            (self.cell_size * y + 1),
                            tab,
                            tab,
                        ),
                    )

    def run(self) -> None:
        screen = curses.initscr()
        curses.noecho()
        screen.clear()
        screen.refresh()
        window = curses.newwin(self.life.rows + 2, self.life.cols + 2)
        self.draw_borders(window)
        window.timeout(1)
        window.nodelay(True)

        running = True
        paused = False
        while running:
            char = window.getch()
            if char == ord("\n"):
                paused = False if paused else True
            elif char == ord("S"):
                self.life.save(self.save_path)
            elif char == curses.ascii.ESC:
                running = False
            if not paused:
                self.draw_grid(window)
                window.refresh()
                self.life.step()

                sleep(1)

        curses.endwin()


if __name__ == "__main__":
    life = GameOfLife((15, 30), randomize=True)
    ui = Console(life, save_path=pathlib.Path("fileui.txt"))
    ui.run()
