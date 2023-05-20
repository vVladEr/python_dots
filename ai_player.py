import time
import dots_player
import bfs


class AI_player(dots_player.Player):
    def __init__(self, level, number, name):
        dots_player.Player.__init__(self, number, name)
        self.level = level

    def get_step(self, player_step, map, used_dots):
        time.sleep(0.2)
        return get_prime_step(player_step, map, used_dots)


def get_prime_step(player_step, map, used_dots):
    for step in bfs.get_neighbours(player_step):
        if step not in used_dots and map.in_bounds(step):
            return step
    return get_default_step(map, used_dots)


def get_default_step(map, used_dots):
    for dot in map.get_all_dots():
        if dot not in used_dots and map.in_bounds(dot):
            return dot
