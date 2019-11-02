import pathlib
import random
import json
import copy

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, size: Tuple[int, int], randomize: bool = True, max_generations: Optional[int] = None) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.n_generation = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        self.curr_generation = []
        next_gen = []
        if randomize:
            next_gen = [[random.randint(0, 1) for i in range(self.rows)] for j in range(self.rows)]
        else:
            next_gen = [[next_gen.append(0) for i in range(self.rows)] for j in range(self.rows)]
        self.curr_generation.append(next_gen)
        return self.curr_generation

    def get_neighbours(self, cell: Cell) -> Cells:
        Cells = []
        x, y = cell
        for row in range(x - 1, x + 1):
            for col in range(y - 1, y + 1):
                if row < 0 or col < 0:
                    continue
                if row >= len(self.curr_generation) or col >= len(self.array[0]):
                    continue
                if row == x and col == y:
                    continue
                Cells.append(self.curr_generation[row][col])
        return Cells

    def get_next_generation(self) -> Grid:

        new_grid = copy.deepcopy(self.curr_generation)
        for i in range(self.roes):
            for j in range(self.cols):
                cell = i, j
                neighbours = self.get_neighbours(cell)
                k = 0
                for t in neighbours:
                    if t == 1:
                        k += 1
                if self.array[i][j] == 0:
                    if k == 3:
                        new_grid[i][j] = 1

                if self.array[i][j] == 1:
                    if k == 3 or k == 2:
                        new_grid[i][j] = 1
                    if k > 3 or k < 2:
                        new_grid[i][j] = 0

        return new_grid
    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = copy.deepcopy(self.create_grid())
        old_grid = self.prev_generation
        self.curr_generation = self.create_grid(randomize=True)
        new_grid = self.curr_generation
        for i in range(self.rows):
            for j in range(self.cols):
                if old_grid[i][j]:
                    if sum(self.get_neighbours((i, j))) in (2, 3):
                        new_grid[i][j] = 1
                    elif sum(self.get_neighbours((i, j))) == 3:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
        self.n_generation += 1
        return new_grid

    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is not None:
            if self.n_generation >= self.max_generations:
                return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.prev_generation[row][col] == self.curr_generation[row][col]:
                    return True
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, 'r') as f:
            ff = json.load(f)
        rows = len(ff)
        cols = len(ff[0])
        game = GameOfLife(size=(rows, cols), randomize=True)
        game.curr_generation = ff
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, 'w') as f:
            json.dump(self.curr_generation, f)