import curses

from homework03.life1 import GameOfLife
from homework03.ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        for i in range(self.life.cols + 1):
            if i == 0 or i == self.life.cols:
                screen.addstr(0, i, '+')
            else:
                screen.addstr(0, i, '-')
        for i in range(1, self.life.rows + 1):
            screen.addstr(i, 0, '|')
            screen.addstr(i, self.life.cols + 1, '|')

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(self.life.cols):
            for j in range(self.life.rows):
                if self.life.curr_generation[i][j] == 1:
                    screen.addstr(i, j, '*')
                else:
                    screen.addstr(i, j, ' ')

    def run(self) -> None:
        screen = curses.initscr()
        self.draw_borders(screen)
        curses.curs_set(0)
        screen.keypad(True)

        self.life.create_grid(True)
        running = True
        while running and self.life.is_changing and \
                not self.life.is_max_generations_exceed:
            self.life.step()
            self.draw_grid(screen)
            screen.refresh()
        curses.endwin()

