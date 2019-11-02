import curses

from homework03.life1 import GameOfLife
from homework03.ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        for i in range(self.width + 1):
            if i == 0 or i == self.width:
                screen.addstr(0, i, '+')
            else:
                screen.addstr(0, i, '-')
        for i in range(1, self.height + 1):
            screen.addstr(i, 0, '|')
            screen.addstr(i, self.width + 1, '|')
        for i in range(self.width + 2):
            if i == 0 or i == self.width + 1:
                screen.addstr(self.height + 1, i, '+')
            else:
                screen.addstr(self.height + 1, i, '-')

    def draw_grid(self, screen) -> None:
        for i in range(self.width):
            for j in range(self.height):
                if self.curr_generation[i][j] == 1:
                    screen.addstr(i, j, '*')
                else:
                    screen.addstr(i, j, ' ')

    def run(self) -> None:
        screen = curses.initscr()
        self.draw_borders(screen)
        self.draw_grid(screen)
        screen.refresh()
        while not self.life.is_max_generations_exceed and self.life.is_changing:
            self.life.step()
            self.draw_grid(screen)
            screen.refresh()
        screen.clear()
        curses.endwin()
