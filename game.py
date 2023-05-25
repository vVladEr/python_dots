import pygame
import pygame_gui
import sys
import game_map
import game_logic
import game_statistic

# размер экрана
SIZE = WIDTH, HEIGHT = game_logic.WIDTH, game_logic.HEIGHT

GRAY = (211, 211, 211)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)

pygame.init()


class Game(game_logic.GameLogic):
    def __init__(self, column_count, line_count):
        game_logic.GameLogic.__init__(self, column_count, line_count)
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

        statistics_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((WIDTH - 200) / 2, 450), (200, 70)),
            text='Game statistics',
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
                        if event.ui_element == statistics_button:
                            running = False
                            self._switch_scene(self._statistic_scene)
                            continue
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

        choose_difficulty_list = pygame_gui.elements.UISelectionList(
                relative_rect=pygame.Rect((WIDTH - 250, HEIGHT - 160), (200, 45)),
                item_list=["Random", "Advanced"],
                manager=gui_manager,
                allow_multi_select=False
        )

        f = pygame.font.SysFont('arial', 24)
        label = f.render("Add players and name each of them", True, BLACK)
        difficulty_label = f.render("Choose Ai difficulty:", True, BLACK)
        self._screen.blit(label, (100, 50))
        self._screen.blit(difficulty_label, (WIDTH-245, HEIGHT - 200))
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
                            ai_difficulty = choose_difficulty_list.get_single_selection()
                            if ai_difficulty == "Advanced":
                                self.ai_difficulty = 1
                            elif ai_difficulty == "Random":
                                self.ai_difficulty = 0
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

    # region STATISTIC_SCENE
    def _statistic_scene(self):
        self._screen.fill(WHITE)

        gui_manager = pygame_gui.UIManager(SIZE)

        f = pygame.font.SysFont('arial', 28, bold=True)
        label = f.render('DOTS GAME STATISTIC', True, BLACK)
        self._screen.blit(label, (280, 30))

        menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((WIDTH - 100) / 2 - 15, 500), (150, 50)),
            text='Back to menu',
            manager=gui_manager
        )

        search_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((550, 100), (150, 40)),
            text='Search',
            manager=gui_manager
        )

        text_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((100, 100), (400, 40)),
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
                        if event.ui_element == menu_button:
                            running = False
                            self._switch_scene(self._menu_scene)

                        if event.ui_element == search_button:
                            name = text_box.get_text().replace('\n', '')
                            saver = game_statistic.StatisticSaver(game_logic.SAVER_FILE_NAME)
                            statistic = saver.get(name)
                            pygame.draw.rect(self._screen, color=WHITE,
                                             rect=pygame.Rect((100, 145), (500, 300)))
                            if statistic is not None:
                                string_statistic = str(statistic)
                                label = f.render(string_statistic, True, BLACK)
                                self._screen.blit(label, (100, 200))
                            else:
                                f = pygame.font.SysFont('arial', 24, bold=False)
                                label = f.render(f'Player {name} not found', True, RED)
                                self._screen.blit(label, (210 - len(name), 150))

                gui_manager.process_events(event)

            gui_manager.draw_ui(self._screen)
            pygame.display.flip()
            gui_manager.update(pygame.time.Clock().tick(60))

    # endregion

    # region GAME_SCENE
    def _create_game_screen(self):
        self._screen.fill(WHITE)
        for rect in self._map.get_net_rectangles():
            pygame.draw.rect(self._screen, GRAY, rect, 1)
        for i in range(len(self._players)):
            self._screen.blit(self._players[i].get_points_text(), (10, 10 + i * 30))
        pygame.display.flip()

    def _draw_player_turn(self):
        pygame.draw.circle(self._screen, self._players[self.current_player].colour,
                           (750, 40), 10)

    def _draw_cycles(self, cycles, colour=None):
        if colour is None:
            colour = self._players[self.current_player].colour
        for cycle in cycles:
            n = len(cycle)
            for i in range(n):
                pygame.draw.line(self._screen, colour, cycle[i], cycle[(i + 1) % n], 3)

    def _redraw_player_points_counter(self, player_index=None):
        i = player_index
        if i is None:
            i = self.current_player
        rect = self._players[i].clear_points_text().get_rect()
        rect.topleft = (10, 10 + i * 30)
        pygame.draw.rect(self._screen, WHITE, rect)
        self._screen.blit(self._players[i].get_points_text(), (10, 10 + i * 30))
        self._players[self.current_player].prev_points = self._players[self.current_player].scores
        pygame.display.flip()

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
                    used_dots = self._players[0].pressed_dots.union(self.caught_dots).union(robot.pressed_dots)
                    pos = robot.get_step(self._last_step,self._players[0].pressed_dots, self._map, used_dots,
                                         self.caught_dots)
                    if pos is not None:
                        is_step_made = True
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            pos = game_map.get_closest_cross(event.pos)
                            if self._map.in_bounds(pos):
                                is_step_made = True
                if is_step_made:
                    is_success, paths = self._try_make_step(pos)
                    if is_success:
                        self._remaining_steps -= 1
                        self._last_step = pos
                        colour = self._players[self.current_player].colour
                        pygame.draw.circle(self._screen, colour, pos, 5)
                        if len(paths) > 0:
                            self._draw_cycles(paths)
                            self._redraw_player_points_counter()
                        else:
                            for enemy in self._players:
                                if enemy.number == self.current_player:
                                    continue
                                enemy_paths = self._find_passive_cycles(pos, enemy)
                                if len(enemy_paths) > 0:
                                    self._draw_cycles(enemy_paths, enemy.colour)
                                    self._redraw_player_points_counter(enemy.number)

                        self._update_player_index()
                        self._draw_player_turn()
            pygame.display.flip()
        if running:
            self._switch_scene(self._end_scene)

    # endregion

    # region END_SCENE
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
        menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((WIDTH - 100) / 2 - 25, (HEIGHT - 50) / 8), (150, 50)),
            text='Back to menu',
            manager=gui_manager
        )

        self._print_results_text()
        self._update_statistic()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == menu_button:
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
