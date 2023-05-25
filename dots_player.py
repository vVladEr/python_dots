import pygame.font

BLUE = (0, 0, 139)
RED = (178, 34, 34)
GREEN = (0, 139, 0)
ORANGE = (255, 120, 30)
WHITE = (255, 255, 255)
PLAYER_COLOURS = {0: BLUE, 1: RED, 2: GREEN, 3: ORANGE}

pygame.font.init()
f = pygame.font.SysFont('arial', 24)


class Player:
    def __init__(self, number, name=None):
        self.number = number
        self.pressed_dots = set()
        self.colour = PLAYER_COLOURS[number]
        self.prev_points = 0
        self.scores = 0
        self.found_cycles = []
        self.name = name
        self.last_step = None
        if name is None:
            self.name = f'Player{self.number + 1}'

    def get_points_text(self):
        return f.render(f'{self.name}: {self.scores}', True, self.colour)

    def clear_points_text(self):
        return f.render(f"{self.name}: {self.prev_points}", True, WHITE)

    def update_found_cycles(self, paths):
        for path in paths:
            self.found_cycles.append(path)
