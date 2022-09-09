import os
import sys

SRC_DIR = os.path.dirname(os.path.abspath(__file__)).replace('test','') + 'src\\'
sys.path.append(SRC_DIR)

from models import *
from functions import *
from settings import *
from sys import exit
from random import getrandbits
import glob
import pygame
import math

pygame.init()
screen = pygame.display.set_mode(screen_size)
print(f"screen size details:\nwidth: {screen_width}, height: {screen_height}"
      f", clock rate: {CLOCK_RATE}")
clock = pygame.time.Clock()

#print(random_point(750))
point = Point(*random_point(750))
target = Point(*random_point(750))

while point.distance(target) < 250:
    target = Point(*random_point(750))

print(point())
print(target())
print(point.distance(target))
index = 1
single_group = pygame.sprite.GroupSingle()
invader = Invader(point(),index, screen)
invader.target_point = target()
single_group.add(invader)

# define target surface-point
target_point = pygame.Surface((32,32))

if __name__ == '__main__':

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill(COLOR_WHITE)
        single_group.update()
        single_group.draw(screen)
        pygame.draw.circle(screen, COLOR_RED, target(), 16)

        pygame.display.update()
        clock.tick(CLOCK_RATE)