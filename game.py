import pygame
import pygame_gui
import sys
import game_map
import dots_player
import bfs


# размер экрана
SIZE = WIDTH, HEIGHT = 800, 600

GRAY = (211, 211, 211)
WHITE = (255, 255, 255)

pygame.init()


class Game:
    def __init__(self, column_count, line_count, players_count):
        self.column_count = column_count
        self.line_count = line_count
        self.players_count = players_count

    def _create_game_screen(self):
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
                self._remaining_steps -= (len(inside_area) - len(enemy_points))
                self._caught_dots = self._caught_dots.union(inside_area)
                player.points += len(enemy_points)
                self._update_player_points_counter()

    def _update_player_points_counter(self):
        i = self.current_player
        rect = self._players[i].clear_points_text().get_rect()
        rect.topleft = (10, 10 + i * 30)
        pygame.draw.rect(self._screen, WHITE, rect)
        self._screen.blit(self._players[i].get_points_text(), (10, 10 + i * 30))
        self._players[self.current_player].prev_points = self._players[self.current_player].points
        pygame.display.flip()

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

    def _switch_scene(self, scene):
        self._current_scene = scene

    def _menu_scene(self):
        self._screen = pygame.display.set_mode(SIZE)
        self._screen.fill(WHITE)

        gui_manager = pygame_gui.UIManager(SIZE)

        small_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((WIDTH - 200) / 7, (HEIGHT - 150) / 2), (200, 150)),
            text='Start 10x10',
            manager=gui_manager
        )

        middle_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((WIDTH - 200) / 2, (HEIGHT - 150) / 2), (200, 150)),
            text='Start 15x15',
            manager=gui_manager
        )

        big_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((WIDTH - 200) * 6 / 7, (HEIGHT - 150) / 2), (200, 150)),
            text='Start 20x20',
            manager=gui_manager
        )

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == big_game_button:
                            self.line_count = 20
                            self.column_count = 20
                        if event.ui_element == middle_game_button:
                            self.line_count = 15
                            self.column_count = 15
                        if event.ui_element == small_game_button:
                            self.line_count = 10
                            self.column_count = 10
                        running = False
                        self._switch_scene(self._game_scene)

                gui_manager.process_events(event)

            gui_manager.draw_ui(self._screen)
            pygame.display.flip()
            gui_manager.update(pygame.time.Clock().tick(60))

    def _init_game(self):
        self._dots = set()
        self._map = game_map.Map(WIDTH, HEIGHT, self.column_count, self.line_count)
        self._remaining_steps = (self.column_count + 1) * (self.line_count + 1)
        self._players = []
        self.players_count = self.players_count
        for i in range(self.players_count):
            player = dots_player.Player(i)
            self._players.append(player)
        self.current_player = 0
        self._caught_dots = set()

    def _end_scene(self):
        gui_manager = pygame_gui.UIManager(SIZE, "theme.json")
        restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((WIDTH - 100) / 2, (HEIGHT - 50) / 8), (100, 50)),
            text='Restart',
            manager=gui_manager
        )

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == restart_button:
                            running = False
                            self._switch_scene(self._menu_scene)

                gui_manager.process_events(event)

            gui_manager.draw_ui(self._screen)
            pygame.display.flip()
            gui_manager.update(pygame.time.Clock().tick(60))

    def _game_scene(self):
        self._init_game()
        self._create_game_screen()
        running = True
        end_flag = False
        while not end_flag and self._remaining_steps > 0 and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self._switch_scene(None)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    end_flag = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = game_map.get_closest_cross(event.pos)
                        if self._map.in_bounds(pos):
                            is_success = self._try_make_step(pos)
                            if is_success:
                                self._remaining_steps -= 1
            pygame.display.flip()
        if running:
            self._switch_scene(self._end_scene)

    def run(self):
        self._switch_scene(self._menu_scene)
        while self._current_scene is not None:
            self._current_scene()
        pygame.quit()
        sys.exit()


def _get_area_inside_cycle(path, pos):
    path_set = set(path)
    inside_point = bfs.find_close_point_inside(path_set, pos, game_map.SQUARE_SIZE)
    if inside_point is None:
        return set()
    return bfs.get_inside_area(path_set, inside_point, game_map.SQUARE_SIZE)
