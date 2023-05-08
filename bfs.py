
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
                        points_queue = _make_new_queue(points_queue, next) # Очень сомнительная штука, но перебор отсекает
                continue
            paths[next] = next_list
            points_queue.append(next_list)


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