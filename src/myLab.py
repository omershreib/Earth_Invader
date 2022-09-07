# Here I checks how sprites or animation response seperately
# I hope that this help me to find scaling and optimisation issues
# beside general errors

from models import Earth
from functions import *
from settings import *
from sys import exit
import glob
import pygame
import math

pygame.init()
screen = pygame.display.set_mode(screen_size)
print(f"screen size details:\nwidth: {screen_width}, height: {screen_height}"
      f", clock rate: {CLOCK_RATE}")
clock = pygame.time.Clock()


if __name__ == '__main__':
    earth = Earth(EARTH_POSITION)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill(COLOR_WHITE)
        earth.update()
        earth.draw(screen)
        pygame.display.update()
        clock.tick(CLOCK_RATE)

