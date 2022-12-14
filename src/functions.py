import pygame
from random import randint, choice
from settings import *

def random_point(radius):
	excluded_radious = radius

	# operating the min/max function just for safty
	min_width = min(screen_width - excluded_radious, screen_width)
	max_width = max(screen_width - excluded_radious, screen_width)
	min_height = min(screen_height - excluded_radious, screen_height)
	max_height = max(screen_height - excluded_radious, screen_height)

	range_left = (0,min_width)
	range_right = (min_width, max_width)
	range_up = (0, min_height)
	range_down = (min_height,max_height)

	rand_x_1 = randint(*range_left)
	rand_x_2 = randint(*range_right)
	rand_y_1 = randint(*range_up)
	rand_y_2 = randint(*range_down)


	point = (choice([rand_x_1,rand_x_2]), choice([rand_y_1, rand_y_2]))
	return point


def define_sprite_movement(vel, distance,self_point, target_point, threshold = 0):
	self_x, self_y = self_point
	target_x, target_y = target_point
	move_x = 0
	move_y = 0

	if distance > threshold:
		if target_x < self_x:
			move_x = -vel

		if target_x >= self_x:
			move_x = vel

		if target_y < self_y:
			move_y = -vel

		if target_y >= self_y:
			move_y = vel

	if distance <= threshold:
		if target_x < self_x:
			move_x = vel

		if target_x >= self_x:
			move_x = -vel

		if target_y < self_y:
			move_y = vel

		if target_y >= self_y:
			move_y = -vel

	# handle the case of x/y line is equal to the x/y's target point
	# so the movement may be smoother
	if target_x == self_x:
		move_x = 0

	if target_y == self_y:
		move_y = 0

	return (move_x, move_y)


def drawCrossHairs(screen, pos):
    # draw cross hairs at the mouse pos
    mx = pos[0]
    my = pos[1]
    pygame.draw.line(screen, COLOR_RED, (mx - 10, my), (mx + 10, my))
    pygame.draw.line(screen, COLOR_RED, (mx, my - 10), (mx, my + 10))


def draw_fire_cross(screen, mouse_position, is_fire, is_reloaded):
    mouse_x, mouse_y = mouse_position

    if is_reloaded:
        color = COLOR_GREY
        pygame.draw.line(screen, color, (mouse_x - 10, mouse_y), (mouse_x - 5, mouse_y))
        pygame.draw.line(screen, color, (mouse_x + 5, mouse_y), (mouse_x + 10, mouse_y))
        pygame.draw.line(screen, color, (mouse_x, mouse_y - 10), (mouse_x, mouse_y - 5))
        pygame.draw.line(screen, color, (mouse_x, mouse_y + 5), (mouse_x, mouse_y + 10))
        return

    if is_fire:
        drawCrossHairs(screen,mouse_position)
        return

    if not is_fire:
        color = COLOR_WHITE
        pygame.draw.line(screen, color, (mouse_x - 10, mouse_y), (mouse_x - 5, mouse_y))
        pygame.draw.line(screen, color, (mouse_x + 5, mouse_y), (mouse_x + 10, mouse_y))
        pygame.draw.line(screen, color, (mouse_x, mouse_y - 10), (mouse_x, mouse_y - 5))
        pygame.draw.line(screen, color, (mouse_x, mouse_y + 5), (mouse_x, mouse_y + 10))