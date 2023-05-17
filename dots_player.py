import pygame.font

BLUE = (0, 0, 139)
RED = (255, 69, 0)
GREEN = (0, 139, 0)
WHITE = (255, 255, 255)
PLAYER_COLOURS = {0: BLUE, 1: RED, 2: GREEN}

pygame.font.init()
f = pygame.font.SysFont('arial', 24)


class Player:
    def __init__(self, number, name=None):
        self.number = number
        self.pressed_dots = set()
        self.colour = PLAYER_COLOURS[number]
        self.prev_points = 0
        self.points = 0
        self.name = name
        if name is None:
            self.name = f'Player{self.number}'

    def get_points_text(self):
        return f.render(f'{self.name}: {self.points}', True, self.colour)

    def clear_points_text(self):
        return f.render(f"{self.name}: {self.prev_points}", True, WHITE)
