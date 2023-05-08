import math

import pygame
import sys
import game_map


# размер экрана
size = width, height = 600, 400

# размер квадратов и цвета
GRAY = (211, 211, 211)
WHITE = (255, 255, 255)
BLUE = (0, 0, 139)
RED = (255, 69, 0)
# инициализация PyGame
pygame.init()


class Game:
    def __init__(self, column_count, line_count):
        self._dots = set()
        # создание окна
        self._screen = pygame.display.set_mode(size)
        # заполнение экрана белым цветом
        self._screen.fill(WHITE)
        self._colour_flag = True
        # количество квадратов по горизонтали и вертикали
        self._column_count = column_count
        self._line_count = line_count
        self._map = game_map.Map(width, height, column_count, line_count)

    def _draw_net(self):
        for rect in self._map.get_net_rectangles():
            pygame.draw.rect(self._screen, GRAY, rect, 1)
        pygame.display.flip()

    def run(self):
        # главный цикл
        self._draw_net()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        colour = RED
                        pos = game_map.get_closest_cross(event.pos)
                        if self._colour_flag:
                            colour = BLUE
                        if pos not in self._dots:
                            self._colour_flag = not self._colour_flag
                            pygame.draw.circle(self._screen, colour, pos, 5)
                            self._dots.add(pos)
                            pygame.display.update()
