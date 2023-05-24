import game_map
import unittest


WIDTH, HEIGHT = 800, 600
COLUMN_COUNT = LINE_COUNT = 4
TEST_MAP = game_map.Map(WIDTH, HEIGHT, COLUMN_COUNT, LINE_COUNT)


class TestMap(unittest.TestCase):
    def testGetNetRectangles(self):
        expected = [(360, 260, 20, 20), (360, 280, 20, 20), (360, 300, 20, 20),
                     (360, 320, 20, 20), (380, 260, 20, 20), (380, 280, 20, 20),
                     (380, 300, 20, 20), (380, 320, 20, 20), (400, 260, 20, 20),
                     (400, 280, 20, 20), (400, 300, 20, 20), (400, 320, 20, 20),
                     (420, 260, 20, 20), (420, 280, 20, 20), (420, 300, 20, 20),
                     (420, 320, 20, 20)]
        result =[rect for rect in TEST_MAP.get_net_rectangles()]
        self.assertEqual(expected, result)

    def testInBounds(self):
        point = (380, 280)
        self.assertTrue(TEST_MAP.in_bounds(point))

    def testNotInBounds(self):
        point = (340, 280)
        self.assertFalse(TEST_MAP.in_bounds(point))

    def testGetAllDots(self):
        expected = {(360, 260), (360, 280), (360, 300), (360, 320), (360, 340), (380, 260),
                    (380, 280), (380, 300), (380, 320), (380, 340), (400, 260), (400, 280),
                    (400, 300), (400, 320), (400, 340), (420, 260), (420, 280), (420, 300),
                    (420, 320), (420, 340), (440, 260), (440, 280), (440, 300), (440, 320),
                    (440, 340)}
        result = {dot for dot in TEST_MAP.get_all_dots()}
        self.assertEqual(expected, result)

    def testGetDistance(self):
        point_1 = (1, 1)
        point_2 = (4, 5)
        expected = 5
        self.assertEqual(expected, game_map.get_distance(point_1, point_2))

    def testGetClosestCross(self):
        position = (405, 337)
        self.assertEqual((400, 340), game_map.get_closest_cross(position))


if __name__ == '__main__':
    unittest.main()
