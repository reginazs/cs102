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

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceeded:
        self.prev_generation = self.curr_generation()
        self.curr_generation = self.get_next_generation()
        self.generations +=1

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
            grid = [[int(x) for x in list(rw)]] for rw in file.readline()]
        row, col = len(grid), len(grid[0])

        game = GameOfLife((row, col))
        game.curr_generation = grid            

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename) as file:
            for row in self.curr_generation:
                file.write(''.join([str(x) for x in row]))
                file.write('\n')
