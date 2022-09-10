import pygame
import math
from sys import exit
from settings import *
from functions import draw_fire_cross
from game import GameManager

pygame.init()
pygame.mixer.init()

BACKGROUND_POSITION = 0,0
EARTH_POSITION = screen_width/2, screen_height/2
CANNON_POSITION = screen_width/2, screen_height/2




def main():
    screen = pygame.display.set_mode(screen_size)
    print(f"screen size details:\nwidth: {screen_width}, height: {screen_height}")
    clock = pygame.time.Clock()

    background = pygame.image.load(background_path).convert()
    background = pygame.transform.smoothscale(background, screen_size)

    pygame.display.set_caption('Earth Invaders')
    game_manager = GameManager(screen)

    fire_flag = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                print('need to fire!')
                if not game_manager.is_cannon_empty:
                    fire_flag = True

            if event.type == pygame.MOUSEBUTTONUP:
                #game_manager.is_fire = False
                fire_flag = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:     # exit the game
                    pygame.quit()
                    exit()

                if event.key == pygame.K_r:     # reload cannon
                    game_manager.reload_cannon()


                if event.key == pygame.K_n:     # call invader wave before time
                    game_manager.is_ready = True

        #screen.fill(COLOR_BLACK)
        screen.blit(background, BACKGROUND_POSITION)
        game_manager.is_fire = fire_flag

        if game_manager.game_life > 0:
            game_manager.run()

        if game_manager.game_life == 0:
            game_manager.game_over()

        draw_fire_cross(screen, pygame.mouse.get_pos(), fire_flag, game_manager.is_reload)
        pygame.display.update()
        clock.tick(CLOCK_RATE)

        #print(pygame.mouse.get_pos())

if __name__ == '__main__':
    main()



