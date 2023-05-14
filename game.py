import pygame
import sys
import game_map
import dots_player
import bfs


# размер экрана
SIZE = WIDTH, HEIGHT = 600, 400

GRAY = (211, 211, 211)
WHITE = (255, 255, 255)

pygame.init()


class Game:
    def __init__(self, column_count, line_count, players_count):
        self._dots = set()
        self._map = game_map.Map(WIDTH, HEIGHT, column_count, line_count)
        self._steps_count = (column_count + 1) * (line_count + 1)
        self._players = []
        self.players_count = players_count
        for i in range(players_count):
            player = dots_player.Player(i)
            self._players.append(player)
        self.current_player = 0
        self._caught_dots = set()

    def _create_start_screen(self):
        self._screen = pygame.display.set_mode(SIZE)
        self._screen.fill(WHITE)
        for rect in self._map.get_net_rectangles():
            pygame.draw.rect(self._screen, GRAY, rect, 1)
        for i in range(len(self._players)):
            self._screen.blit(self._players[i].get_points_text(), (10, 10 + i * 30))
        pygame.display.flip()

    def _update_player_index(self):
        self.current_player += 1
        self.current_player %= self.players_count

    def _is_used_point(self, dot):
        for player in self._players:
            if dot in player.pressed_dots:
                return True
        return False

    def _try_make_step(self, pos):
        if pos in self._caught_dots:
            return False
        if self._is_used_point(pos):
            return False
        player = self._players[self.current_player]
        colour = player.colour
        pygame.draw.circle(self._screen, colour, pos, 5)
        pygame.display.update()
        player.pressed_dots.add(pos)
        self._try_find_catching_cycle(pos)
        self._update_player_index()
        return True

    def _try_find_catching_cycle(self, pos):
        player = self._players[self.current_player]
        non_caught_dots = player.pressed_dots.difference(self._caught_dots)
        cycles = bfs.find_cycles(pos, non_caught_dots)
        for cycle in cycles:
            path_list = list(cycle)
            inside_area = _get_area_inside_cycle(path_list, pos)
            inside_area = inside_area.difference(self._caught_dots)
            enemy_points = self._intersect_enemy_dots(inside_area, player)
            if len(enemy_points) > 0:
                self._draw_shape(path_list)
                self._caught_dots = self._caught_dots.union(inside_area)
                player.points += len(enemy_points)
                # НЕОБХОДИМО ДОПИСАТЬ ОБНОВЛЕНИЕ ЭКРАНА С ОЧКАМИ

    def _intersect_enemy_dots(self, area_inside_cycle, current_player):
        enemy_points = set()
        for enemy in self._players:
            if enemy.number == current_player.number:
                continue
            enemy_intersection = area_inside_cycle.intersection(enemy.pressed_dots)
            enemy_points = enemy_points.union(enemy_intersection)
        return enemy_points

    def _draw_shape(self, cycle):
        colour = self._players[self.current_player].colour
        n = len(cycle)
        for i in range(n):
            pygame.draw.line(self._screen, colour, cycle[i], cycle[(i+1) % n], 3)
        pygame.display.update()

    def run(self):
        self._create_start_screen()
        while self._steps_count > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = game_map.get_closest_cross(event.pos)
                        if self._map.in_bounds(pos):
                            is_success = self._try_make_step(pos)
                            if is_success:
                                self._steps_count += 1


def _get_area_inside_cycle(path, pos):
    path_set = set(path)
    inside_point = bfs.find_close_point_inside(path_set, pos, game_map.SQUARE_SIZE)
    if inside_point is None:
        return set()
    return bfs.get_inside_area(path_set, inside_point, game_map.SQUARE_SIZE)
