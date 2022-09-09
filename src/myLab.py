# Here I checks how sprites or animation response seperately
# I hope that this help me to find scaling and optimisation issues
# beside general errors

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


if __name__ == '__main__':
    earth = Earth(EARTH_POSITION)
    clouds = Clouds()
    flag = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill(COLOR_WHITE)
        earth.update()
        earth.draw(screen)

        clouds.update()
        clouds.draw(screen)

        # clouds display
        # clouds.update()
        # if not clouds.is_annomation_play:
        #     if bool(getrandbits(1)):
        #         clouds.is_annomation_play = True
        # if clouds.is_annomation_play:
        #     clouds.draw(screen)

        pygame.display.update()
        clock.tick(CLOCK_RATE)

