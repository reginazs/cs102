import random
import typing as tp

import pygame

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    """
    Business logic class
    """

    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        self.grid = self.create_grid()

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x_c in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x_c, 0), (x_c, self.height))
        for y_c in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y_c), (self.width, y_c))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_grid()
            self.draw_lines()

            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def is_alive(self, cell: Cell) -> bool:
        """
        Checks if a cell is alive
        """
        return bool(self.grid[cell[0]][cell[1]])

    def _is_a_cell(self, cell: Cell) -> bool:
        """
        Checks a cell for coordinate validity
        """
        return 0 <= cell[0] < len(self.grid) and 0 <= cell[1] < len(self.grid[0])

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:
            return [
                [random.randint(0, 1) for x in range(self.cell_width)]
                for _ in range(self.cell_height)
            ]
        else:
            return [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for x in range(self.cell_width):
            for y in range(self.cell_height):
                if self.grid[y][x] != 0:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (
                            (self.cell_size * x),
                            (self.cell_size * y),
                            self.cell_size,
                            self.cell_size,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (
                            (self.cell_size * x),
                            (self.cell_size * y),
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbors = []
        shifts = ((i, j) for i in (-1, 2) for j in (-1, 2))
        for x, y in shifts:
            if (x, y) == (0, 0):
                continue
            row, col = cell[0] + x, cell[1] + y
            if self._is_a_cell((row, col)):
                neighbors.append(int(self.is_alive((row, col))))
        return neighbors

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_gen = self.create_grid(False)
        for x in range(self.cell_height):
            for y in range(self.cell_width):
                new_ngbrs = self.get_neighbours((x, y)).count(1)
                if self.grid[x][y] == 0 and new_ngbrs == 3:
                    new_gen[x][y] = 1
                elif self.grid[x][y] == 1 and new_ngbrs in [2, 3]:
                    new_gen[x][y] = 1
        return new_gen


if __name__ == "__main__":
    game = GameOfLife(640, 480, 20)
    game.run()
