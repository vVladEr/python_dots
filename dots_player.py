
BLUE = (0, 0, 139)
RED = (255, 69, 0)
PLAYER_COLOURS = {0: BLUE, 1: RED}


class Player:
    def __init__(self, number):
        self.numder = number
        self.pressed_dots = set()
        self.colour = PLAYER_COLOURS[number]