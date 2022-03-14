import pygame
from pygame.locals import *
from homework03.life import GameOfLife
from homework03.ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int = 50, speed: int=10) -> None:
        super().__init__(life)

        self.cell_size = cell_size
        self.width = self.life.rows * self.cell_size
        self.height = self.life.cols * self.cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    color_cell = pygame.Color('green')
                    rects = Rect((j * self.cell_size) + 1, (i * self.cell_size) + 1, self.cell_size - 1,
                                 self.cell_size - 1)
                    pygame.draw.rect(self.screen, color_cell, rects)
                else:
                    color_cell = pygame.Color('white')
                    rects = Rect((j * self.cell_size) + 1, (i * self.cell_size) + 1, self.cell_size - 1,
                                 self.cell_size - 1)
                    pygame.draw.rect(self.screen, color_cell, rects)

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('black'))

        running = True
        pause = False
        while running and not self.life.is_max_generations_exceed and self.life.is_changing:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYUP and event.key == K_SPACE:
                    pause = not pause
                elif event.type == MOUSEBUTTONUP and pause:
                    j, i = pygame.mouse.get_pos()
                    i = i // self.cell_size
                    j = j // self.cell_size
                    if self.life.curr_generation[i][j] == 1:
                        self.life.curr_generation[i][j] = 0
                    else:
                        self.life.curr_generation[i][j] = 1

            self.draw_grid()
            self.draw_lines()
            if not pause:
                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()




if __name__ == '__main__':
    ui = GUI(GameOfLife((40, 40), True, 100))
    ui.run()