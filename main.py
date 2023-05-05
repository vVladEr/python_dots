import math

import pygame
import sys

# размер экрана
size = width, height = 600, 400
# количество квадратов по горизонтали и вертикали
n = width // 20
m = height // 20
# размер квадратов и цвета
square_size = 20
grey = (211, 211, 211)
white = (255, 255, 255)
blue = (0, 0, 139)
red = (255, 69, 0)
colour_flag = True

dots = set()
# инициализация PyGame
pygame.init()

# создание окна
screen = pygame.display.set_mode(size)

# заполнение экрана белым цветом
screen.fill(white)

# создание сетки черного цвета
rect_x = (width - n * square_size) // 2
rect_y = (height - m * square_size) // 2
for i in range(n):
    for j in range(m):
        rect = pygame.Rect(i * square_size, j * square_size, square_size, square_size)
        pygame.draw.rect(screen, grey, rect, 1)

# обновление экрана
pygame.display.flip()


def get_dist(dot1, dot2):
    dx = dot1[0] - dot2[0]
    dy = dot1[1] - dot2[1]
    return math.sqrt(dx*dx + dy*dy)



def get_closest_cross(pos):
    temp_x = (pos[0] // square_size) * square_size
    temp_y = (pos[1] // square_size) * square_size
    cur_dist = get_dist(pos, (temp_x, temp_y))
    cross_pos = [temp_x, temp_y]
    for dx in range(2):
        for dy in range(2):
            x_pos = temp_x + dx * square_size
            y_pos = temp_y+dy * square_size
            dist = get_dist(pos, (x_pos, y_pos))
            if dist < cur_dist:
                cur_dist = dist
                cross_pos[0] = x_pos
                cross_pos[1] = y_pos
    return tuple(cross_pos)


# главный цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                colour = red
                pos = get_closest_cross(event.pos)
                if colour_flag:
                    colour = blue
                if pos not in dots:
                    colour_flag = not colour_flag
                    pygame.draw.circle(screen, colour, pos, 5)
                    dots.add(pos)
                    pygame.display.update()





