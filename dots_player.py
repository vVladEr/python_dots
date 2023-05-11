import pygame.font

BLUE = (0, 0, 139)
RED = (255, 69, 0)
PLAYER_COLOURS = {0: BLUE, 1: RED}

pygame.font.init()
f = pygame.font.SysFont("arial", 24)

class Player:
    def __init__(self, number):
        self.number = number
        self.pressed_dots = set()
        self.colour = PLAYER_COLOURS[number]
        self.points = 0

    def get_points_text(self):
        return f.render(f"Player{self.number}: {self.points}", True, self.colour)
