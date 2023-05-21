import bfs
import unittest


TEST_SET_1 = {(0, 1), (1, 0), (1, 2), (2, 1)}
TEST_SET_2 = {(0, 1), (1, 0), (1, 2), (2, 1), (-1, 0), (-1, 2), (-2, 1)}
TEST_SET_3 = {(0, 1), (1, 0), (1, 2), (2, 2), (2, 0), (3, 1)}
START_POINT = (0, 1)
INSIDE_POINT = (1, 1)
TEST_DISTANCE = 1


class TestBFS(unittest.TestCase):
    def testSimpleFindCycles(self):
        cycles = [cycle for cycle in bfs.find_cycles(START_POINT, TEST_SET_1, TEST_DISTANCE)]
        self.assertEqual(len(cycles), 1)
        cycle = cycles[0]
        self.assertEqual(set(cycle), TEST_SET_1)

    def testFindCyclesWithTwoCycles(self):
        cycles = [cycle for cycle in bfs.find_cycles(START_POINT, TEST_SET_2, TEST_DISTANCE)]
        self.assertEqual(len(cycles), 2)
        expected1 = TEST_SET_2.difference(TEST_SET_1)
        expected1.add(START_POINT)
        cycle1 = cycles[0]
        self.assertEqual(set(cycle1), expected1)
        cycle2 = cycles[1]
        self.assertEqual(set(cycle2), TEST_SET_1)

    def testGetInsideArea(self):
        result = bfs.get_inside_area(TEST_SET_3, INSIDE_POINT, TEST_DISTANCE)
        expected = {(1, 1), (2, 1)}
        self.assertEqual(result, expected)

    def testGetPossibleDirections(self):
        directions = [_ for _ in bfs._get_possible_directions(INSIDE_POINT, TEST_DISTANCE)]
        self.assertEqual(set(directions), TEST_SET_1)

    def testFindPointInside(self):
        point = bfs.find_close_point_inside(TEST_SET_3, START_POINT, TEST_DISTANCE)
        self.assertEqual(point, INSIDE_POINT)

    def testFindNoPoint(self):
        point = bfs.find_close_point_inside(TEST_SET_3.union({INSIDE_POINT}), START_POINT, TEST_DISTANCE)
        self.assertEqual(point, None)

    def testIsLimited(self):
        result = bfs._is_limited(INSIDE_POINT, TEST_SET_1, TEST_DISTANCE)
        self.assertTrue(result)

    def testIsNotLimited(self):
        result = bfs._is_limited((0, 0), TEST_SET_1, TEST_DISTANCE)
        self.assertFalse(result)

    def testMaxAndMin(self):
        result = bfs.get_max_and_min(TEST_SET_3, lambda x: x[0])
        self.assertEqual(result, (3, 0))

    def testCanHavePointInside(self):
        result1 = bfs._can_have_point_inside(TEST_SET_1, TEST_DISTANCE)
        self.assertTrue(result1)
        result2 = bfs._can_have_point_inside(TEST_SET_1.difference({(1, 2)}), TEST_DISTANCE)
        self.assertFalse(result2)

    def testGetNeighbours(self):
        neighbours = {_ for _ in bfs.get_neighbours((0, 0), TEST_DISTANCE)}
        self.assertEqual(len(neighbours), 8)
        excpected = {(0, 1), (0, -1), (1, 1), (1, 0),
                     (1, -1), (-1, 1), (-1, 0), (-1, -1)}
        self.assertEqual(excpected, neighbours)

    def testMergePaths(self):
        l1 = bfs.SinglyLinkedList(3, None)
        l1 = bfs.SinglyLinkedList(2, l1)

        l2 = bfs.SinglyLinkedList(3, None)
        l2 = bfs.SinglyLinkedList(1, l2)

        result = list(bfs._merge_paths(l1, l2))
        self.assertEqual([1, 2, 3], result)


class TestSinglyLinkedList(unittest.TestCase):
    def testDoubleIteration(self):
        l = bfs.SinglyLinkedList(2, None)
        l = bfs.SinglyLinkedList(1, l)
        first = list(l)
        second = list(l)
        self.assertEqual(first, [1, 2])
        self.assertEqual(first, second)

    def testProperties(self):
        l = bfs.SinglyLinkedList(3, None)
        l = bfs.SinglyLinkedList(2, l)
        l = bfs.SinglyLinkedList(1, l)
        self.assertEqual(l.length, 3)
        self.assertEqual(l.second, 2)


if __name__ == '__main__':
    unittest.main()
