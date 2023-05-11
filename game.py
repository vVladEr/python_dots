
import pygame
import sys
import game_map
import dots_player
import  bfs


# размер экрана
size = width, height = 600, 400

GRAY = (211, 211, 211)
WHITE = (255, 255, 255)

pygame.init()

class Game:
    def __init__(self, column_count, line_count, players_count):
        self._dots = set()
        # количество квадратов по горизонтали и вертикали
        self._map = game_map.Map(width, height, column_count, line_count)
        self._steps_count = (column_count + 1) * (line_count + 1)
        self._players = []
        self.players_count = players_count
        for i in range(players_count):
            player = dots_player.Player(i)
            self._players.append(player)
        self.current_player = 0

    def _create_start_screen(self):
        self._screen = pygame.display.set_mode(size)
        self._screen.fill(WHITE)
        for rect in self._map.get_net_rectangles():
            pygame.draw.rect(self._screen, GRAY, rect, 1)
        for i in range(len(self._players)):
            self._screen.blit(self._players[i].get_points_text(), (10, 10 + i * 30))
            #edge = 10
            #if i % 2:
            #    edge = 450
            #self._screen.blit(self._players[i].get_points_text(), (edge, 10 + i // 2 * 30))
        pygame.display.flip()

    def _update_player_index(self):
        self.current_player += 1
        self.current_player %= self.players_count

    def _is_not_used_point(self, dot):
        for player in self._players:
            if dot in player.pressed_dots:
                return False
        return True

    def _try_make_step(self, pos):
        player = self._players[self.current_player]
        colour = player.colour
        if self._is_not_used_point(pos):
            pygame.draw.circle(self._screen, colour, pos, 5)
            pygame.display.update()
            player.pressed_dots.add(pos)
            self._try_find_cycle(pos)
            self._update_player_index()
            return True
        return False

    def _try_find_cycle(self, pos):
        player = self._players[self.current_player]
        cycles = bfs.find_cycles(pos, player.pressed_dots)
        for cycle in cycles:
            route = [x for x in cycle]
            if len(route):
                self._draw_shape(route)

    def _draw_shape(self, cycle):
        colour = self._players[self.current_player].colour
        for i in range(len(cycle)-1):
            pygame.draw.line(self._screen, colour, cycle[i], cycle[i+1], 3)
            pygame.display.update()
        pygame.draw.line(self._screen, colour, cycle[-1], cycle[0], 3)
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
