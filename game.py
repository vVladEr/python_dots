import pygame
import pygame_gui
import sys
import game_map
import dots_player
import bfs
import ai_player


# размер экрана
SIZE = WIDTH, HEIGHT = 800, 600

GRAY = (211, 211, 211)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)

pygame.init()


class Game:
    def __init__(self, column_count, line_count):
        self.column_count = column_count
        self.line_count = line_count
        self.players_names = []
        self._screen = pygame.display.set_mode(SIZE)

    def _switch_scene(self, scene):
        self._current_scene = scene

    # region MENU_SCENE
    def _menu_scene(self):
        self._screen.fill(WHITE)

        gui_manager = pygame_gui.UIManager(SIZE)

        small_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((WIDTH - 200) / 7, (HEIGHT - 150) / 2), (200, 150)),
            text='Start 10x10',
            manager=gui_manager
        )

        middle_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((WIDTH - 200) / 2, (HEIGHT - 150) / 2), (200, 150)),
            text='Start 16x16',
            manager=gui_manager
        )

        big_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((WIDTH - 200) * 6 / 7, (HEIGHT - 150) / 2), (200, 150)),
            text='Start 20x20',
            manager=gui_manager
        )

        small_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((WIDTH - 200) / 7, (HEIGHT - 150) / 2), (200, 150)),
            text='Start 10x10',
            manager=gui_manager
        )

        f = pygame.font.SysFont('arial', 36, bold=True)
        label = f.render("DOTS GAME", True, BLACK)
        self._screen.blit(label, (310, 70))

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
                            self.line_count = 16
                            self.column_count = 16
                        if event.ui_element == small_game_button:
                            self.line_count = 10
                            self.column_count = 10
                        running = False
                        self._switch_scene(self._name_players_scene)

                gui_manager.process_events(event)

            gui_manager.draw_ui(self._screen)
            pygame.display.flip()
            gui_manager.update(pygame.time.Clock().tick(60))

    def _name_players_scene(self):
        self._screen.fill(WHITE)

        gui_manager = pygame_gui.UIManager(SIZE)

        add_player_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH - 200, 150), (40, 40)),
            text='+',
            manager=gui_manager
        )

        remove_player_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH - 200, 200), (40, 40)),
            text='-',
            manager=gui_manager
        )

        go_to_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH - 250, HEIGHT - 100), (200, 40)),
            text='Start the game',
            manager=gui_manager
        )

        f = pygame.font.SysFont('arial', 24)
        label = f.render("Add players and name each of them", True, BLACK)
        self._screen.blit(label, (100, 50))
        text_boxes = []

        text_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((200, 150 + len(text_boxes) * 50), (200, 40)),
            manager=gui_manager)
        text_boxes.append(text_box)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self._switch_scene(None)
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == go_to_game_button:
                            player_names = [box.get_text().replace('\n', '') for box in text_boxes]
                            for i in range(len(player_names)):
                                if player_names[i] == '':
                                    player_names[i] = None
                            running = False
                            self.players_names = player_names
                            self._switch_scene(self._game_scene)
                        if event.ui_element == remove_player_button:
                            if len(text_boxes) > 1:
                                text_boxes[-1].kill()
                                del text_boxes[-1]
                                gui_manager.update(0)
                                rect = pygame.Rect((200, 150 + len(text_boxes) * 50), (200, 40))
                                pygame.draw.rect(self._screen, WHITE, rect)
                        if event.ui_element == add_player_button:
                            if len(text_boxes) < 4:
                                text_box = pygame_gui.elements.UITextEntryBox(
                                            relative_rect=pygame.Rect((200, 150 + len(text_boxes) * 50), (200, 40)),
                                            manager=gui_manager)
                                text_boxes.append(text_box)
                gui_manager.process_events(event)

            gui_manager.draw_ui(self._screen)
            pygame.display.flip()
            gui_manager.update(pygame.time.Clock().tick(60))

    # endregion

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
            robot = ai_player.AI_player(0, 1, name='Robot')
            self._players.append(robot)
            self.players_count += 1
        self.with_robot = type(self._players[1]) is ai_player.AI_player
        self.current_player = 0
        self._caught_dots = set()

    def _create_game_screen(self):
        self._screen.fill(WHITE)
        for rect in self._map.get_net_rectangles():
            pygame.draw.rect(self._screen, GRAY, rect, 1)
        for i in range(len(self._players)):
            self._screen.blit(self._players[i].get_points_text(), (10, 10 + i * 30))
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

    def _update_player_points_counter(self):
        i = self.current_player
        rect = self._players[i].clear_points_text().get_rect()
        rect.topleft = (10, 10 + i * 30)
        pygame.draw.rect(self._screen, WHITE, rect)
        self._screen.blit(self._players[i].get_points_text(), (10, 10 + i * 30))
        self._players[self.current_player].prev_points = self._players[self.current_player].points
        pygame.display.flip()

    def _is_used_point(self, dot):
        for player in self._players:
            if dot in player.pressed_dots:
                return True
        return False

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

    def _update_player_index(self):
        self.current_player += 1
        self.current_player %= self.players_count

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
                is_step_made = False
                pos = (0, 0)
                if self.with_robot and self.current_player == 1:
                    robot = self._players[1]
                    used_dots = self._players[0].pressed_dots.union(self._caught_dots).union(robot.pressed_dots)
                    pos = robot.get_step(self._last_step, self._map, used_dots)
                    if pos is not None:
                        is_step_made = True
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            pos = game_map.get_closest_cross(event.pos)
                            if self._map.in_bounds(pos):
                                is_step_made = True
                if is_step_made:
                    is_success = self._try_make_step(pos)
                    if is_success:
                        self._remaining_steps -= 1
                        self._last_step = pos
            pygame.display.flip()
        if running:
            self._switch_scene(self._end_scene)

    # endregion

    # region END_SCENE
    def _get_winner_or_default(self):
        is_draw = max(self._players, key=lambda x: x.points) == min(self._players, key=lambda x: x.points)
        if is_draw:
            return None
        return max(self._players, key=lambda x: x.points)

    def _print_results_text(self):
        winner = self._get_winner_or_default()
        results_text = 'Draw! Friendship won!'
        if winner is not None:
            results_text = f'{winner.name} won!'
        x = WIDTH // 2 - len(results_text) * 5
        f = pygame.font.SysFont('arial', 24, bold=True)
        label = f.render(results_text, True, BLACK)
        self._screen.blit(label, (x, 10))

    def _end_scene(self):
        gui_manager = pygame_gui.UIManager(SIZE, "theme.json")
        restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((WIDTH - 100) / 2 - 25, (HEIGHT - 50) / 8), (150, 50)),
            text='Back to menu',
            manager=gui_manager
        )

        self._print_results_text()

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

    # endregion

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
