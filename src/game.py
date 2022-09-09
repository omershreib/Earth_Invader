import pygame
import math
from sys import exit
from settings import *
from models import *
from utilities import *
from functions import *



# text-fonts
SCORE_TEXT = "SCORE:"
SHELL_TEXT = "BULLETS:"

#SCORE_FONT = pygame.font.Font(font_path, 40)
#SHELL_FONT = pygame.font.Font(font_path, 32)


class GameManager:
    def __init__(self, surface):
        # general
        self.display_surface = surface
        self.game_score = 0
        self.game_life = 100
        self.max_cannon_shells = 15

        # cannon details
        self.is_cannon_empty = False
        self.current_shellnum = self.max_cannon_shells
        self.is_fire = False
        self.is_reload = False
        self.reload_speed = 10 # smaller the number increase reload speed
        self.reload_baseline = 0
        self.cannon_status = 'Ready'
        self.float_precision = 3

        self.fire_rate = 0.25  # fire/sec
        self.last_fire = round(time.perf_counter(), self.float_precision)

        # font initanilzation
        self.SCORE_FONT = pygame.font.Font(font_path, 40)
        self.SHELL_FONT = pygame.font.Font(font_path, 32)
        self.CANNON_STATUS_FONT = pygame.font.Font(font_path, 32)
        self.LIFT_FONT = pygame.font.Font(font_path, 32)

        # invaders stuff
        self.invaders_ID = 1

        # setup game sprites
        self.game_setup()

        # invaders comming definition
        self.invaders_to_summon = 1
        self.next_summon_level = 2
        self.last_summon = round(time.perf_counter(), self.float_precision)
        self.summon_rate = 5 # summons/sec, summons number is increased

    def call_invader(self):
        invader_sprite = Invader(random_point(750), self.invaders_ID, self.display_surface)
        self.invaders_ID += 1
        self.invaders.add(invader_sprite)

    def game_setup(self):
        self.cannon = Cannon()
        self.earth = pygame.sprite.GroupSingle()
        self.shells = pygame.sprite.Group()
        self.invaders = pygame.sprite.Group()
        self.clouds = Clouds()


        earth_sprite = Earth(EARTH_POSITION)
        self.earth.add(earth_sprite)

    def reload_cannon(self):
        if self.current_shellnum == self.max_cannon_shells:
            print("cannon is fully reloded")
            self.cannon_status = "Ready"
            self.is_reload = False
            self.is_cannon_empty = False

        if self.current_shellnum < self.max_cannon_shells:
            self.is_reload = True
            self.is_cannon_empty = True     # raise this flag also if reload command pressed
            if self.reload_baseline == self.reload_speed:
                self.current_shellnum += 1
                self.reload_baseline = 0
            self.reload_baseline += 1

    def display_texts(self):
        self.update_score()
        self.update_bullets_num()
        self.update_cannon_status()
        self.update_life_status()

    def update_life_status(self):
        score_text = self.SCORE_FONT.render(f'LIFE: {self.game_life}', True, COLOR_WHITE)
        self.display_surface.blit(score_text, SCORE_TEXT_POSOTION)

    def update_cannon_status(self):
        if not self.is_cannon_empty:
            self.cannon_status = "Ready"

        if self.is_cannon_empty:
            if self.is_reload:
                self.cannon_status = "Reload"

            if not self.is_reload:
                self.cannon_status = 'Empty'


        cannon_text = self.CANNON_STATUS_FONT.render(f'Status: {self.cannon_status}', True, COLOR_WHITE)
        self.display_surface.blit(cannon_text, CANNON_STATUS_TEXT_POSOTION)

    def update_score(self):
        score_text = self.SCORE_FONT.render(f'SCORE: {self.game_score}', True, COLOR_WHITE)
        self.display_surface.blit(score_text, LIFE_TEXT_POSOTION)

    def update_bullets_num(self):
        bullets_num = self.current_shellnum
        shell_text = self.SHELL_FONT.render(f'BULLETS: {bullets_num}', True, COLOR_WHITE)
        self.display_surface.blit(shell_text, SHELL_TEXT_POSOTION)

    def round_time(self, *args):
        n = len(args)
        fp = self.float_precision
        if n == 1:
            return round(args[0], fp)

        if n == 2:
            return round(abs(args[0] - args[1]), fp)

    def run(self):
        screen = self.display_surface

        # cannon fire
        #result = round(time.perf_counter() - self.last_fire, self.float_precision)
        if self.round_time(time.perf_counter(), self.last_fire) > self.fire_rate:
            if self.is_fire:
                if not self.is_reload:
                    self.last_fire = self.round_time(time.perf_counter())

                    # check if cannon in reload process
                    if self.current_shellnum > 0:   # check if there any bullet
                        self.shells.add(CannonShell(self.cannon))
                        self.current_shellnum -=1

        # check if empty
        if self.current_shellnum == 0:
            self.is_cannon_empty = True

        # check for reload
        if self.is_reload:
            self.reload_cannon()

        self.shells.update()
        self.is_fire = False

        # cannon
        self.cannon.update(pygame.mouse.get_pos())
        self.cannon.draw(screen)

        # earth
        self.earth.update(screen)
        self.earth.draw(screen)

        # clouds
        self.clouds.update()
        self.clouds.draw(screen)

        # shells
        self.shells.draw(screen)

        # invaders summon
        if self.round_time(time.perf_counter(), self.last_summon) > self.summon_rate:
            [self.call_invader() for i in range(self.invaders_to_summon)]
            self.invaders_to_summon += self.next_summon_level
            self.summon_rate += 10

        # invaders update
        self.invaders.update()
        self.invaders.draw(screen)

        for invader in self.invaders:
            if pygame.sprite.spritecollide(invader, self.shells, True):
                invader.is_exploded = True

        if not bullet_hits.empty():
            if self.game_life > 0:

                # play hit animation
                for e in self.earth:
                    self.game_life -= bullet_hits.get()
                    e.hit(screen)
                #print('hit!')

            if self.game_life <= 0:
                self.game_life = 0
                #print('dead')

        self.display_texts()



