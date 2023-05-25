import time
import dots_player
import bfs
import random


class AI_player(dots_player.Player):
    def __init__(self, level, number, name):
        dots_player.Player.__init__(self, number, name)
        self.level = level

    def get_step(self, player_step, map, used_dots, caught_dots):
        time.sleep(0.2)
        return get_smart_step(player_step, map, used_dots, caught_dots)


def get_prime_step(player_step, map, used_dots):
    steps = list(bfs.get_neighbours(player_step))
    n = random.randint(0, 8)
    for i in range(n, n + 8):
        step = steps[i % len(steps)]
        if step == player_step:
            continue
        if step not in used_dots and map.in_bounds(step):
            return step
    return get_default_step(map, used_dots)


def get_default_step(map, used_dots):
    for dot in map.get_all_dots():
        if dot not in used_dots and map.in_bounds(dot):
            return dot


def get_smart_step(enemy_dots, map, used_dots, caught_dots):
    max_points_around = -1
    best_dot = None
    for dot in enemy_dots:
        if dot in caught_dots or not _has_empty_space(dot, used_dots, map):
            continue
        neighbours = list(bfs.get_neighbours(dot))
        near_friendlies = 0
        for neighbour in neighbours:
            if neighbour in used_dots and neighbour not in enemy_dots:
                near_friendlies += 1
        if near_friendlies >= max_points_around:
            max_points_around = near_friendlies
            best_dot = dot
    steps = _get_directions_in_priority(best_dot, map)
    for step in steps:
        if step == best_dot:
            continue
        if step not in used_dots and map.in_bounds(step):
            return step
    print("default_step")
    return get_default_step(map, used_dots)


def _get_directions_in_priority(dot, map):
    res = []
    pos_dir = list(bfs.get_possible_directions(dot))
    for dir in pos_dir:
        if map.in_bounds(dir):
            res.append(dir)

    neighbors = bfs.get_neighbours(dot)
    for neighbor in neighbors:
        if neighbor not in res and map.in_bounds(neighbor):
            res.append(neighbor)
    return res


def _has_empty_space(dot, used_dots, map):
    neighbours = list(bfs.get_neighbours(dot))
    for neighbour in neighbours:
        if neighbour not in used_dots and map.in_bounds(neighbour):
            return True
    return False


