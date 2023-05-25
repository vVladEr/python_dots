class StepInfo:
    def __init__(self, dot):
        self.pressed_dot = dot
        self.found_cycles_info = []


class CycleInfo:
    def __init__(self, cycle, caught_area, player_number, scores):
        self.cycle = cycle
        self.caught_area = caught_area
        self.player_number = player_number
        self.scores = scores
