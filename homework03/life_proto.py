import pygame
import random

from pygame.locals import *
from typing import List, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
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

    def draw_lines(self) -> None:
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('black'))
        self.array = self.create_grid(randomize=True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()
            self.draw_grid(self.array)
            self.array = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

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
        self.array = []
        self.array = [[0] * self.cell_width for i in range(self.cell_height)]
        if randomize == True:
            self.array = [[random.randint(0, 1) for i in range(self.cell_width)] for j in range(self.cell_height)]
        else:
            self.array = [[random.randint(0) for i in range(self.cell_width)] for j in range(self.cell_height)]
        return self.array

    def draw_grid(self, array: list) -> List:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):

                if array[i][j] == 1:
                    color_cell = pygame.Color('green')
                    rects = Rect((j * self.cell_size) + 1, (i * self.cell_size) + 1, self.cell_size - 1,
                                 self.cell_size - 1)
                    pygame.draw.rect(self.screen, color_cell, rects)
                if array[i][j] == 0:
                    color_cell = pygame.Color('white')
                    rects = Rect((j * self.cell_size) + 1, (i * self.cell_size) + 1, self.cell_size - 1,
                                 self.cell_size - 1)
                    pygame.draw.rect(self.screen, color_cell, rects)

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
        Cells = []
        x, y = cell
        for row in range(x - 1, x + 2):
            for col in range(y - 1, y + 2):
                if row < 0 or col < 0:
                    continue
                if row >= len(self.array) or col >= len(self.array[0]):
                    continue
                if row == x and col == y:
                    continue
                Cells.append(self.array[row][col])
        return Cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_array = [[0] * self.cell_width for i in range(self.cell_height)]

        for i in range(self.cell_height):
            for j in range(self.cell_width):
                cell = i, j
                neighbours = self.get_neighbours(cell)
                k = 0
                for t in neighbours:
                    if t == 1:
                        k += 1
                if self.array[i][j] == 0:
                    if k == 3:
                        new_array[i][j] = 1

                if self.array[i][j] == 1:
                    if k == 3 or k == 2:
                        new_array[i][j] = 1
                    if k > 3 or k < 2:
                        new_array[i][j] = 0

        return new_array

if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()