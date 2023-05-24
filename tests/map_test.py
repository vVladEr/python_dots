import game_map
import unittest


WIDTH, HEIGHT = 800, 600
COLUMN_COUNT = LINE_COUNT = 4
TEST_MAP = game_map.Map(WIDTH, HEIGHT, COLUMN_COUNT, LINE_COUNT)


class TestMap(unittest.TestCase):
    def testGetNetRectangles(self):
        pass


if __name__ == '__main__':
    unittest.main()