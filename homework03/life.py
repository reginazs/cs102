import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def is_alive(self, cell: Cell) -> bool:
        """
        Checks if a cell is alive
        """
        return bool(self.curr_generation[cell[0]][cell[1]])

    def _is_a_cell(self, cell: Cell) -> bool:
        """
        Checks a cell for coordinate validity
        """
        return 0 <= cell[0] < len(self.curr_generation) and 0 <= cell[1] < len(
            self.curr_generation[0]
        )

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
            return [[random.randint(0, 1) for x in range(self.cols)] for _ in range(self.rows)]
        else:
            return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

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
        for x in range(self.cols):
            for y in range(self.rows):
                new_ngbrs = self.get_neighbours((x, y)).count(1)
                if self.curr_generation[x][y] == 0 and new_ngbrs == 3:
                    new_gen[x][y] = 1
                elif self.curr_generation[x][y] == 1 and new_ngbrs in [2, 3]:
                    new_gen[x][y] = 1
        return new_gen

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation[:]
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if not self.max_generations:
            return False
        return self.max_generations <= self.generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename) as file:
            grid = [[int(x) for x in list(rw)] for rw in file.readline()]
        row, col = len(grid), len(grid[0])

        game = GameOfLife((row, col))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename) as file:
            for row in self.curr_generation:
                file.write("".join([str(x) for x in row]))
                file.write("\n")
