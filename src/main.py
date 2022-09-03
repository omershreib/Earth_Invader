import pygame
import math
from sys import exit
from settings import *
from game import GameManager

BACKGROUND_POSITION = 0,0
EARTH_POSITION = screen_width/2, screen_height/2
CANNON_POSITION = screen_width/2, screen_height/2


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


def main():
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    print(f"screen size details:\nwidth: {screen_width}, height: {screen_height}")
    clock = pygame.time.Clock()

    background = pygame.image.load(background_path).convert()
    background = pygame.transform.smoothscale(background, screen_size)

    pygame.display.set_caption('Earth Invaders')
    game_manager = GameManager(screen)

    # tests
    test_surface = pygame.Surface((16,16))
    cannon_pivot = pygame.draw.circle(test_surface, COLOR_BLACK, (8,8), 8)
    fire_flag = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_manager.is_cannon_empty:
                    game_manager.is_fire = True
                    fire_flag = True

            if event.type == pygame.MOUSEBUTTONUP:
                fire_flag = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:     # exit the game
                    pygame.quit()
                    exit()

                if event.key == pygame.K_r:     # reload cannon
                    game_manager.reload_cannon()

                if event.key == pygame.K_i:     # add invader
                    game_manager.call_invader()



        #screen.fill(COLOR_WHITE)
        screen.blit(background, BACKGROUND_POSITION)
        #pygame.draw.ellipse(screen, (0,255,0),(130, 500, 60, 120))
        game_manager.run()
        draw_fire_cross(screen, pygame.mouse.get_pos(), fire_flag, game_manager.is_reload)
        pygame.display.update()
        clock.tick(CLOCK_RATE)

        #print(pygame.mouse.get_pos())

if __name__ == '__main__':
    main()



