import game_logic
import dots_player
import game_map
import unittest


WIDTH, HEIGHT = 800, 600


class TestMap(unittest.TestCase):
    def setUp(self):
        players = [dots_player.Player(i) for i in range(2)]
        self.game = game_logic.GameLogic(4, 4)
        players[0].pressed_dots.add((80, 80))
        cycle = {(100, 100), (80, 120), (100, 140), (120, 120)}
        players[0].pressed_dots = players[0].pressed_dots.union(cycle)
        players[1].pressed_dots.add((100, 120))
        self.game._players = players
        self.game.current_player = 0
        self.game.caught_dots = {(60, 60)}
        self.game.players_count = 2
        self.game._dots = set()
        self.game._map = game_map.Map(WIDTH, HEIGHT, self.game.column_count,
                                            self.game.line_count)
        self.game._remaining_steps = (self.game.column_count + 1) * (self.game.line_count + 1)

    def testUpdatePlayerIndex(self):
        current = self.game.current_player
        self.game._update_player_index()
        self.assertEqual(current + 1, self.game.current_player)
        self.game.current_player = current

    def testGetWinner(self):
        players = self.game._players
        players[0].scores = 5
        players[1].scores = 4
        self.assertEqual(0, self.game._get_winner_or_default().number)

    def testGetWinnerWhenDraw(self):
        players = self.game._players
        players[0].scores = 5
        players[1].scores = 5
        self.assertEqual(None, self.game._get_winner_or_default())

    def testGetAreaInsideCycle(self):
        cycle = {(0, 20), (20, 0), (20, 40), (40, 20), (-20, 0), (-20, 40), (-40, 20)}
        start_point = (20, 0)
        result = game_logic._get_area_inside_cycle(cycle, start_point)
        self.assertEqual({(20, 20)}, result)

    def testIntersectEnemyDots(self):
        enemy = self.game._players[0]
        player = self.game._players[1]
        expected = {(20, 40), (40, 40)}
        enemy.pressed_dots = enemy.pressed_dots.union(expected)
        area_inside = {(20, 20), (20, 40), (40, 20), (40, 40)}
        result = self.game._intersect_enemy_dots(area_inside, player)
        self.assertEqual(expected, result)

    def testIsUsed(self):
        point = (80, 80)
        self.assertTrue(self.game._is_used_point(point))

    def testIsNotUsed(self):
        point = (60, 20)
        self.assertFalse(self.game._is_used_point(point))

    def testFindCatchingCycle(self):
        position = (100, 100)
        self.game.current_player = 0
        expected = [(80, 120), (100, 140), (120, 120), (100, 100)]
        success, cycles = list(self.game._try_find_catching_cycle(position))
        self.assertTrue(success)
        self.assertEqual(1, len(cycles))
        self.assertEqual(expected, cycles[0])

    def testMakeStepInUsedDot(self):
        point = (80, 80)
        success, paths = self.game._try_make_step(point)
        self.assertFalse(success)
        self.assertEqual(None, paths)

    def testMakeStepInNonactiveZone(self):
        point = (60, 60)
        success, paths = self.game._try_make_step(point)
        self.assertFalse(success)
        self.assertEqual(None, paths)

    def testRightStep(self):
        point = (80, 60)
        success, paths = self.game._try_make_step(point)
        self.assertTrue(success)
        self.assertEqual([], paths)

    def testFindPassiveCycles(self):
        self.game.current_player = 1
        position = (100, 100)
        expected = [(80, 120), (100, 140), (120, 120), (100, 100)]
        cycles = self.game._find_passive_cycles(position, self.game._players[0])
        self.assertEqual(1, len(cycles))
        self.assertEqual(expected, cycles[0])


if __name__ == '__main__':
    unittest.main()
