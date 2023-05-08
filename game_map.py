import math


SQUARE_SIZE = 20


class Map:
    def __init__(self, screen_width, screen_height, column_count, line_count):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._column_count = column_count
        self._line_count = line_count

    def get_net_rectangles(self):
        rect_x = (self.screen_width - self._column_count * SQUARE_SIZE) // 2
        rect_y = (self.screen_height - self._line_count * SQUARE_SIZE) // 2
        for i in range(self._column_count):
            for j in range(self._line_count):
                rect = (rect_x + i * SQUARE_SIZE, rect_y + j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                yield rect


def get_dist(dot1, dot2):
    dx = dot1[0] - dot2[0]
    dy = dot1[1] - dot2[1]
    return math.sqrt(dx*dx + dy*dy)


def get_closest_cross(pos):
    temp_x = (pos[0] // SQUARE_SIZE) * SQUARE_SIZE
    temp_y = (pos[1] // SQUARE_SIZE) * SQUARE_SIZE
    cur_dist = get_dist(pos, (temp_x, temp_y))
    cross_pos = [temp_x, temp_y]
    for dx in range(2):
        for dy in range(2):
            x_pos = temp_x + dx * SQUARE_SIZE
            y_pos = temp_y + dy * SQUARE_SIZE
            dist = get_dist(pos, (x_pos, y_pos))
            if dist < cur_dist:
                cur_dist = dist
                cross_pos[0] = x_pos
                cross_pos[1] = y_pos
    return tuple(cross_pos)