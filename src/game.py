import re

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


class Level:
    def __init__(self):

        # invaders comming definition
        self.wave_num = 0  # the number of wave
        self.wave_size = 1      # how many invaders to summon
        self.next_summon_level = 2
        self.float_precision = 3  # define floating-point accuracy for optimisation
        self.last_summon = round(time.perf_counter(), self.float_precision)
        self.summon_rate = 5    # summons/sec, summons number increases during the game
        self.next_wave_time = -1     # time left until the next wave

    def call_invader(self, num, init_next_wave = False):
        """call <num> invaders to attack earth"""

        for i in range(num):
            invader_sprite = Invader(random_point(750), self.invaders_ID, self.display_surface)
            self.invaders.add(invader_sprite)
            self.invaders_ID += 1

        if init_next_wave:
            # define the upcoming invaders wave
            self.init_next_wave()

    def init_next_wave(self):
        """define next invaders wave"""
        self.wave_num += 1
        self.wave_size += self.next_summon_level
        self.last_summon = self.round_time(time.perf_counter())
        self.summon_rate += 5


class TextDisplay:
    """manage all the text display in the screen during the game"""

    def __init__(self, surface):
        # font initanilzation
        self.SCORE_FONT = pygame.font.Font(font_path, 40)
        self.SHELL_FONT = pygame.font.Font(font_path, 32)
        self.CANNON_STATUS_FONT = pygame.font.Font(font_path, 32)
        self.LIFT_FONT = pygame.font.Font(font_path, 32)

    def display_texts(self):
        self.update_score()
        self.update_bullets_num()
        self.update_cannon_status()
        self.update_life_status()
        self.update_next_wave()
        self.update_wave_num()

    def update_wave_num(self):
        wave_num = self.SHELL_FONT.render(f'#WAVE: {self.wave_num}', True, COLOR_WHITE)
        self.display_surface.blit(wave_num, WAVW_NUM_TEXT_POSITION)

    def update_next_wave(self):
        next_wave_time = self.SHELL_FONT.render(f'NEXT WAVE: {self.next_wave_time}', True, COLOR_WHITE)
        self.display_surface.blit(next_wave_time, NEXT_WAVE_TEXT_POSITION)

    def update_life_status(self):
        score_text = self.SHELL_FONT.render(f'LIFE: {self.game_life}', True, COLOR_WHITE)
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
        score_text = self.SHELL_FONT.render(f'SCORE: {self.game_score}', True, COLOR_WHITE)
        self.display_surface.blit(score_text, LIFE_TEXT_POSOTION)

    def update_bullets_num(self):
        bullets_num = self.current_shellnum
        shell_text = self.SHELL_FONT.render(f'BULLETS: {bullets_num}', True, COLOR_WHITE)
        self.display_surface.blit(shell_text, SHELL_TEXT_POSOTION)


class GameManager(TextDisplay, Level):
    """(almost) all the game settings been configurated here"""

    def __init__(self, surface):

        TextDisplay.__init__(self,surface)
        Level.__init__(self)

        # generals
        self.display_surface = surface
        self.game_score = 0
        self.game_life = 100

        # cannon details
        self.max_cannon_shells = 15
        self.current_shellnum = self.max_cannon_shells
        self.is_cannon_empty = False    # maunly needed for text displament puprose
        self.is_fire = False
        self.is_reload = False
        self.is_ready = False   # player ready for the next invader wave (increase score)
        self.reload_speed = 10  # smaller the number increase reload speed
        self.reload_baseline = 0
        self.cannon_status = 'Ready'    # 3-statuses: Ready, Empty and Reloded


        self.fire_rate = 0.25  # fire/sec
        self.last_fire = round(time.perf_counter(), self.float_precision)   # this control auto-fire during mouse-key been pressed

        # invaders stuff
        self.invaders_ID = 1    # currently used on Invader.__str__(), probably this unnecesary

        # setup game sprites
        self.game_setup()

    def game_setup(self):
        self.cannon = Cannon()
        self.earth = pygame.sprite.GroupSingle()
        self.shells = pygame.sprite.Group()
        self.invaders = pygame.sprite.Group()
        self.clouds = Clouds()


        earth_sprite = Earth(EARTH_POSITION)
        self.earth.add(earth_sprite)

    def game_over(self):
        game_over_text = self.SCORE_FONT.render(f'GAME OVER', True, COLOR_WHITE)
        self.display_surface.blit(game_over_text, [screen_width/2, screen_height/2 - 25])

        score_text = self.SHELL_FONT.render(f'SCORE: {self.game_score}', True, COLOR_WHITE)
        self.display_surface.blit(score_text, [screen_width/2, screen_height/2 + 25])

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

        # time until next summon
        self.next_wave_time = self.summon_rate - int(self.round_time(time.perf_counter(), self.last_summon))

        # player is brave! call wave before time
        if self.is_ready and self.next_wave_time > 0:
            self.game_score += self.next_wave_time * self.wave_num
            self.is_ready = False
            self.call_invader(self.wave_size, True)

        # call wave on time
        if self.next_wave_time <= 0:
            self.call_invader(self.wave_size, True)

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

            if self.game_life <= 0:
                self.game_life = 0

        # update score
        if not invaders_kill.empty():
            self.game_score += invaders_kill.get()

        # display text
        self.display_texts()



