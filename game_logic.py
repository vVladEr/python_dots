import game_map
import dots_player
import bfs
import ai_player
import game_statistic
from step_cancel import StepInfo, CycleInfo


# размер экрана
SIZE = WIDTH, HEIGHT = 800, 600

SAVER_FILE_NAME = 'game_statistic_saver'


class GameLogic:
    def __init__(self, column_count, line_count):
        self.column_count = column_count
        self.line_count = line_count
        self.players_names = []
        self.ai_difficulty = 0
        self._current_step = None

    # region GAME_SCENE
    def _init_game(self):
        self._dots = set()
        self._map = game_map.Map(WIDTH, HEIGHT, self.column_count, self.line_count)
        self._remaining_steps = (self.column_count + 1) * (self.line_count + 1)
        self._players = []
        self.players_count = len(self.players_names)
        for i in range(self.players_count):
            player = dots_player.Player(i, self.players_names[i])
            self._players.append(player)
        if self.players_count == 1:
            robot = ai_player.AI_player(self.ai_difficulty, 1, name='Robot')
            self._players.append(robot)
            self.players_count += 1
        self.with_robot = type(self._players[1]) is ai_player.AI_player
        self.current_player = 0
        self._caught_dots = set()

    def _intersect_enemy_dots(self, area_inside_cycle, current_player):
        enemy_points = set()
        for enemy in self._players:
            if enemy.number == current_player.number:
                continue
            enemy_intersection = area_inside_cycle.intersection(enemy.pressed_dots)
            enemy_points = enemy_points.union(enemy_intersection)
        return enemy_points

    def _is_used_point(self, dot):
        for player in self._players:
            if dot in player.pressed_dots:
                return True
        return False

    def _try_find_catching_cycle(self, pos, player=None):
        if player is None:
            player = self._players[self.current_player]
        non_caught_dots = player.pressed_dots.difference(self._caught_dots)
        cycles = bfs.find_cycles(pos, non_caught_dots)
        flag = False
        paths = []
        for cycle in cycles:
            path_list = list(cycle)
            inside_area = _get_area_inside_cycle(path_list, pos)
            inside_area = inside_area.difference(self._caught_dots)
            enemy_points = self._intersect_enemy_dots(inside_area, player)
            if len(enemy_points) > 0:
                paths.append(path_list)
                self._remaining_steps -= (len(inside_area) - len(enemy_points))
                self._caught_dots = self._caught_dots.union(inside_area)
                player.scores += len(enemy_points)

                cycle_info = CycleInfo(path_list, inside_area, player.number, len(enemy_points))
                self._current_step.found_cycles_info.append(cycle_info)
                flag = True
        return flag, paths

    def _update_player_index(self):
        self.current_player += 1
        self.current_player %= self.players_count

    def _try_undo_step(self):
        current_player = self.current_player
        self.current_player = (self.current_player - 1) % self.players_count
        player = self._players[self.current_player]
        last_step = player.last_step
        if last_step is None:
            self.current_player = current_player
            return False

        self._remaining_steps += 1
        player.pressed_dots.remove(last_step.pressed_dot)
        for cycle_info in last_step.found_cycles_info:
            self._remaining_steps += len(cycle_info.caught_area)
            self._caught_dots = self._caught_dots.difference(cycle_info.caught_area)
            self._players[cycle_info.player_number].found_cycles.remove(cycle_info.cycle)
            self._remaining_steps -= cycle_info.scores
            p = self._players[cycle_info.player_number]
            p.scores -= cycle_info.scores

        player.last_step = None
        if type(player) is ai_player.AI_player:
            self._try_undo_step()
        return True

    def _try_make_step(self, pos):
        if pos in self._caught_dots:
            return False, None
        if self._is_used_point(pos):
            return False, None
        self._current_step = StepInfo(pos)
        player = self._players[self.current_player]
        player.pressed_dots.add(pos)
        _, paths = self._try_find_catching_cycle(pos)
        self._remaining_steps -= 1
        return True, paths

    def _find_passive_cycles(self, enemy_pos, enemy):
        max_x, _ = bfs.get_max_and_min(enemy.pressed_dots, lambda point: point[0])
        x = enemy_pos[0]
        while x <= max_x:
            current_pos = (x, enemy_pos[1])
            if current_pos in enemy.pressed_dots:
                return self._try_find_catching_cycle(current_pos, enemy)[1]
            x += game_map.SQUARE_SIZE
        return []

    # endregion

    # region END_SCENE
    def _get_winner_or_default(self):
        is_draw = max(self._players, key=lambda x: x.scores) == min(self._players, key=lambda x: x.scores)
        if is_draw:
            return None
        return max(self._players, key=lambda x: x.scores)

    def _update_statistic(self):
        saver = game_statistic.StatisticSaver(SAVER_FILE_NAME)
        winner = self._get_winner_or_default()
        if winner is None:
            for player in self._players:
                saver.update_player_statistic(player, False, True)
        else:
            saver.update_player_statistic(winner, True)
            for loser in self._players:
                if loser.name == winner.name:
                    continue
                saver.update_player_statistic(loser, False)

    # endregion


def _get_area_inside_cycle(path, pos):
    path_set = set(path)
    inside_point = bfs.find_close_point_inside(path_set, pos, game_map.SQUARE_SIZE)
    if inside_point is None:
        return set()
    return bfs.get_inside_area(path_set, inside_point, game_map.SQUARE_SIZE)
