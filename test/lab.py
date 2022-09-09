import os
import sys

SRC_DIR = os.path.dirname(os.path.abspath(__file__)).replace('test','') + 'src\\'
sys.path.append(SRC_DIR)


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

    invader = Inv
    flag = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(CLOCK_RATE)

