from collections import deque


def find_cycles(start_point, points_set, distance=20):
    points_queue = deque()
    points_queue.append(SinglyLinkedList(start_point))
    paths = dict()
    merged_points = set()
    while len(points_queue) != 0:
        current_list = points_queue.popleft()
        for next in get_neighbours(current_list.value, distance):
            if current_list.previous is not None and next == current_list.previous.value:
                continue
            if next not in points_set:
                continue
            next_list = SinglyLinkedList(next, current_list)
            if next in paths:
                if next not in merged_points:
                    merged_points.add(next)
                    merged_points.add(next_list.previous.value)
                    result = _merge_paths(next_list.previous, paths[next])
                    if len(result) > 3:
                        yield result
                        points_queue = _make_new_queue(points_queue, next)
                continue
            paths[next] = next_list
            points_queue.append(next_list)


def get_inside_area(path_set, point_inside, distance=1):
    stack = [point_inside]
    result = set()
    while len(stack) > 0:
        current_point = stack.pop()
        result.add(current_point)
        for new_point in _get_possible_directions(current_point, distance):
            if new_point in path_set or new_point in result:
                continue
            stack.append(new_point)
    return result


def _get_possible_directions(current_point, distance=1):
    yield current_point[0], current_point[1] + distance
    yield current_point[0], current_point[1] - distance
    yield current_point[0] + distance, current_point[1]
    yield current_point[0] - distance, current_point[1]


def find_close_point_inside(path_set, current_point, distance=1):
    max_y, min_y = get_max_and_min(path_set, lambda x: x[1])
    # if not(_have_point_inside(path_set, max_y, min_y, distance)):
    #     return None

    for point in get_neighbours(current_point, distance):
        if point in path_set:
            continue
        if _is_limited(point, path_set, distance, max_y, min_y):
            return point
    return None


def _is_limited(point, path_set, distance=1, max_y=None, min_y=None):
    max_x, min_x = get_max_and_min(path_set, lambda x: x[0])
    if max_y is None or min_y is None:
        max_y, min_y = get_max_and_min(path_set, lambda x: x[1])

    flag = True
    x, y = point
    while x >= min_x:
        x -= distance
        if (x, y) in path_set:
            break
    else:
        flag = False

    x, y = point
    while x <= max_x:
        x += distance
        if (x, y) in path_set:
            break
    else:
        flag = False

    x, y = point
    while y >= min_y:
        y -= distance
        if (x, y) in path_set:
            break
    else:
        flag = False

    x, y = point
    while y <= max_y:
        y += distance
        if (x, y) in path_set:
            break
    else:
        flag = False

    return flag


def get_max_and_min(collection, selector=lambda x: x):
    max_value = 0
    min_value = 10**8
    for item in collection:
        new_value = selector(item)
        max_value = max(max_value, new_value)
        min_value = min(min_value, new_value)
    return max_value, min_value


def _create_y_levels(path, max_y, min_y, distance=1):
    y_levels = [[] for _ in range((max_y - min_y + distance) // distance)]
    for point in path:
        x = point[0]
        y_levels[(point[1] - min_y) // distance].append(x)
    return y_levels


def _have_point_inside(path, max_y, min_y, distance=1):
    y_levels = _create_y_levels(path, max_y, min_y, distance)
    if len(y_levels) < 3:
        return False
    for level in y_levels:
        for i in range(len(level) - 1):
            if abs(level[i + 1] - level[i]) > distance:
                return True
    return False


def _merge_paths(first, second):
    result = first
    n = len(second)
    for item in second:
        n -= 1
        if n > 0:
            result = SinglyLinkedList(item, result)
    return result


def _make_new_queue(queue, parent):
    if len(queue) == 0:
        return queue
    result = deque()
    while len(queue) > 0:
        last = queue.popleft()
        if last.value == parent:
            continue
        result.append(last)
    return result


def get_neighbours(current, distance=1):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == dy == 0:
                continue
            yield current[0] + dx * distance, current[1] + dy * distance


class SinglyLinkedList:
    def __init__(self, value, previous=None):
        self.value = value
        self.previous = previous
        self.length = 1
        if previous is not None:
            self.length += len(previous)
        self._current = self

    def __len__(self):
        return self.length

    def __str__(self):
        return f'value: {self.value}, count: {self.length}'

    def __iter__(self):
        self._current = self
        return self

    def __next__(self):
        if self._current is None:
            raise StopIteration
        result = self._current.value
        self._current = self._current.previous
        return result


if __name__ == '__main__':
    # Для дебага
    s = set()
    s.add((1,0))
    s.add((0,1))
    s.add((2,0))
    s.add((3,1))
    s.add((3,2))
    s.add((2,2))
    s.add((1,2))
    for c in find_cycles((1,2), s, 1):
        for i in c:
            print(i)
        print('__')

    if True:
        print(':::::::::::')
        s = set()
        s.add((1,0))
        s.add((0,1))
        s.add((2,1))
        s.add((1,2))
        s.add((2,2))
        s.add((0,0))
        s.add((0,2))
        s.add((2,0))

        for c in find_cycles((1,0), s, 1):
            for i in c:
                print(i)
            print('__')

    if True:
        s = set()
        s.add((0, 1))
        s.add((1, 0))
        s.add((0, 2))
        s.add((0, 3))
        s.add((1, 4))
        s.add((2, 1))
        s.add((2, 2))
        s.add((2, 3))
        s.add((2, 2))

        p = find_close_point_inside(s, (0, 1))
        print(f'point: {p}')
        area = get_inside_area(s, p)
        print(area)

        l = SinglyLinkedList(1)
        l = SinglyLinkedList(2, l)
        for i in l:
            print(i)
        print(':::::::::')
        for i in l:
            print(i)
