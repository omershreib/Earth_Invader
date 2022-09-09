import pygame
import math
from pygame.math import Vector2
from settings import *
from utilities import import_folder
from math import sin, cos
from random import randint, getrandbits
from functions import random_point, define_sprite_movement
from multiprocessing import Queue
import time
import glob
import re


bullet_hits = Queue()

class Clouds(pygame.sprite.Sprite):
    def __init__(self, pos = EARTH_POSITION):
        super().__init__()

        # define animation
        self.animation_assetes = {'idle': []}
        self.animation_imgpath = '../graphic/img/clouds/'
        self.animation_baseline = 36
        self.animation_curr_line = 0
        self.frame_index = 0
        self.clock_frames = 6
        self.annimation_wait_baseline = 600
        self.annimation_wait_index = 0
        self.is_idle_play = False

        # import all annimations
        [self.load_animations(name) for name in self.animation_assetes.keys()]

        # scaling assets
        for key in self.animation_assetes:
            for i, asset in enumerate(self.animation_assetes[key]):
                self.animation_assetes[key][i] = pygame.transform.scale(asset, earth_scale).convert_alpha()

        # generals
        self.image = self.animation_assetes['idle'][0]  # idle is the default image
        self.rect = self.image.get_rect(center=pos)


    def load_animations(self, key):
        img_list = []
        filepath = self.animation_imgpath + key
        # [img_list.append(pygame.image.load(img).convert_alpha()) for img in glob.glob(f'{filepath}\*.png')]
        [img_list.append(img) for img in glob.glob(f'{filepath}\*.png')]
        img_list.sort(key=lambda x: int(re.findall(r'\d+\.png', x)[0].replace('.png', '')))

        self.animation_assetes[key] = [pygame.image.load(img).convert_alpha() for img in img_list]

    def idle(self):
        "while earth is spinning and healthy, until death :|"

        n = len(self.animation_assetes['idle'])
        if self.frame_index < n:
            if self.animation_baseline < self.animation_curr_line:

                self.animation_curr_line = 0
                self.frame_index += 1
                self.image = self.animation_assetes['idle'][self.frame_index]

        if self.frame_index == n - 1: # restart the animation from the first frame
            self.is_idle_play = False
            self.frame_index = 0

        self.animation_curr_line += self.clock_frames

    def update(self):
        # playing the clouds animation at a random time
        # hopfullty this will provide more realistice image of earth
        self.idle()
        
        # if self.annimation_wait_baseline <= self.annimation_wait_index:
        #     self.is_idle_play = True
        #     self.annimation_wait_index = 0
        #
        # if self.annimation_wait_baseline > self.annimation_wait_index:
        #     self.annimation_wait_index += 1


    def draw(self, surface):
        #if self.is_idle_play:
        surface.blit(self.image, self.rect)



class Background(pygame.sprite.Sprite):
    def __init__(self, filepath):
        super().__init__()
        self.image = pygame.image.load(background_path)
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0


class Cannon(pygame.sprite.Sprite):
    def __init__(self):
        image = pygame.image.load('../graphic/img/cannon/Cannon2.png').convert_alpha()
        self.cannonIm = pygame.transform.smoothscale(image, cannon_size).convert_alpha()
        self.pivot = CANNON_POSITION
        self.angle = 0
        self.aimCannon()

    def aimCannon(self):
        # rotate the cannon image around the pivot
        self.image = pygame.transform.rotate(self.cannonIm, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pivot

    def update(self, mPos):
        # set angle between the cannon and mouse pos
        yDiff = self.rect.centery - mPos[1]
        xDiff = mPos[0] - self.rect.centerx
        self.angle = math.atan2(yDiff, xDiff) * 180. / math.pi
        # print(int(self.angle))
        self.aimCannon()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class CannonShell(pygame.sprite.Sprite):
    def __init__(self, cannon):
        super().__init__()

        # define cannon-shell surface
        self.image = pygame.Surface((16, 16))
        self.image.set_colorkey(COLOR_BLACK)
        pygame.draw.circle(self.image, COLOR_RED, (8, 8), 5)  # red ball
        self.rect = self.image.get_rect()

        # generals
        self.velocity = 10
        self.damage = 5


        self.radAngle = math.pi * cannon.angle / 180.       # radian movement
        barrelLen = cannon.cannonIm.get_width() / 2         # distance from cannon
        self.rect.center = \
            (cannon.pivot[0] + barrelLen * cos(self.radAngle),
             cannon.pivot[1] - barrelLen * sin(self.radAngle))

    def update(self):
        vel = self.velocity
        self.rect = self.rect.move(vel * cos(self.radAngle), -vel * sin(self.radAngle)) # fire


class Earth(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # define animation
        self.animation_assetes = {'idle': []}
        self.animation_imgpath = '../graphic/img/earth/'
        self.animation_baseline = 360
        self.animation_curr_line = 0
        self.frame_index = 1
        self.clock_frames = 30
        self.last_time = 0

        # import all annimations
        [self.load_animations(name) for name in self.animation_assetes.keys()]

        # scaling assets
        for key in self.animation_assetes:
            for i, asset in enumerate(self.animation_assetes[key]):
                scaled_asset = pygame.transform.scale(asset, earth_scale).convert_alpha()
                self.animation_assetes[key][i] = pygame.transform.rotate(scaled_asset, 23.44)


        # generals
        self.image = self.animation_assetes['idle'][0]  # idle is the default image
        self.rect = self.image.get_rect(center = pos)
        self.idle_n = len(self.animation_assetes['idle'])

    def load_animations(self, key):
        img_list = []
        filepath = self.animation_imgpath + key
        #[img_list.append(pygame.image.load(img).convert_alpha()) for img in glob.glob(f'{filepath}\*.png')]
        [img_list.append(img) for img in glob.glob(f'{filepath}\*.png')]
        img_list.sort(key=lambda x: int(re.findall(r'\d+\.png', x)[0].replace('.png', '')))

        self.animation_assetes[key] = [pygame.image.load(img).convert_alpha() for img in img_list]

    def idle(self):
        "while earth is spinning and healthy, until death :|"
        n = self.idle_n
        if self.animation_baseline == self.animation_curr_line:
            if self.frame_index < n:
                self.animation_curr_line = 0
                self.image = self.animation_assetes['idle'][self.frame_index]
                self.frame_index += 1

            if self.frame_index == n: # restart the animation from the first frame
                self.frame_index = 1

        self.animation_curr_line += self.clock_frames

    def update(self):
        self.idle()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Bullets(pygame.sprite.Sprite):
    def __init__(self, invader_pos, target = EARTH_POSITION):
        super().__init__()

        # define ivader-bullet surface
        self.image = pygame.Surface((8, 8))
        self.image.set_colorkey(COLOR_BLACK)
        pygame.draw.circle(self.image, COLOR_LIME, (5,5), 2)
        self.rect = self.image.get_rect()
        self.damage = 1

        # define movement
        self.pos = self.x, self.y = invader_pos
        self.target = target
        self.velocity = 10

        # killing definitions
        self.time = time.time()
        self.time_to_kill = 5

        self.fix_angle()

    def fix_angle(self):
        vel = self.velocity

        y_diff = self.target[1] - self.y
        x_diff = self.y - self.target[0]

        angle = math.atan2(y_diff, x_diff)  # angle in radians

        if self.x < self.target[0]:             # invader LEFT to target
            self.dx = -vel * math.cos(angle)
            self.dy = vel * math.sin(angle)

        if self.x >= self.target[0]:            # invader RIGHT to target
            self.dx = vel * math.cos(angle)
            self.dy = vel * math.sin(angle)

    def collision(self, radious = 50):

        target_x = self.target[0]
        target_y = self.target[1]
        collision_range_x = range(int(target_x - radious), int(target_x + radious))
        collision_range_y = range(int(target_y - radious), int(target_y + radious))

        if self.x in collision_range_x and self.y in collision_range_y:
            bullet_hits.put(self.damage)
            #print(f'bullet {self} it!')

    def update(self):
        vel = self.velocity
        # self.x and self.y are floats, so the firing movement is more accurate
        # if converting them to an intagers
        self.x += int(self.dx)
        self.y += int(self.dy)

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.collision()
        self.kill_sprite()

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def kill_sprite(self):
        if time.time() - self.time > self.time_to_kill:
            self.kill()


class Invader(pygame.sprite.Sprite):
    def __init__(self, pos, id, screen):
        super().__init__()

        # define animation
        self.animation_assetes = {'idle': [], 'exploded': []}
        self.animation_imgpath = '../graphic/img/invaders/'
        self.animation_baseline = 30
        self.animation_curr_line = 0
        self.frame_index = 0
        self.clock_frames = 15

        # import all annimations
        [self.load_animations(name) for name in self.animation_assetes.keys()]

        # scaling assets
        for key in self.animation_assetes:
            for i, asset in enumerate(self.animation_assetes[key]):
                self.animation_assetes[key][i] = pygame.transform.scale(asset, scaling_size).convert_alpha()

        # generals
        self.image = self.animation_assetes['idle'][0] # idle is the default image
        self.oirign_img = self.image
        self.rect = self.image.get_rect(center=pos)
        self.target_point = EARTH_POSITION
        self.id = id
        self.surface = screen


        # charactericstices
        self.health = 100
        self.fire_damage = 1
        self.velocity = 1
        self.vel_baseline = 3
        self.vel_curr_baseline = 0
        self.is_exploded = False

        # bullets definitions
        self.bullets = pygame.sprite.Group()
        self.fire_baseline = 100
        self.fire_loading_speed = 5
        self.fire_curr_baseline = 100

        # movement
        self.movement_baseline = 100
        self.movement_speed = 10

        # distance from earth thresholds
        self.dfe_threshold = 150
        self.dfe_factor = 2
        self.is_move_toward_earth = True
        self.get_position()


    def get_position(self):
        return self.rect.centerx, self.rect.centery

    def fire(self):
        baseline = self.fire_baseline
        curr_baseline = self.fire_curr_baseline
        if curr_baseline == baseline:
            bullet = Bullets(self.get_position())
            self.bullets.add(bullet)
            self.fire_curr_baseline = 0

        if curr_baseline < baseline:
            curr_baseline += self.fire_loading_speed

        self.bullets.update()
        self.bullets.draw(self.surface)

    def get_distance_from_point(self, point=EARTH_POSITION):
        point_x, point_y = point
        self_x, self_y = self.rect.centerx, self.rect.centery
        x_diff =  point_x - self_x
        y_diff = self_y - point_y

        distance = (x_diff**2 + y_diff**2)**0.5
        return distance

    def move_toward_point(self, point=EARTH_POSITION):
        vel = self.velocity
        distance = self.get_distance_from_point()

        threshold = self.dfe_threshold if self.is_move_toward_earth else 0
        self_position = self_x, self_y = self.rect.centerx, self.rect.centery
        movement = define_sprite_movement(vel, distance, self_position, self.target_point, threshold)
        self.rect = self.rect.move(movement)

    def load_animations(self, key):
        img_list = []
        filepath =  self.animation_imgpath + key
        [img_list.append(pygame.image.load(img).convert_alpha()) for img in glob.glob(f'{filepath}\*.png')]

        self.animation_assetes[key] = img_list

    def exploded(self):
        n = len(self.animation_assetes['exploded'])

        self.image = self.animation_assetes['exploded'][self.frame_index]
        if self.frame_index < n:
            if self.animation_baseline < self.animation_curr_line:
                self.animation_curr_line = 0
                self.frame_index += 1

                if self.frame_index >= n:   # killing sprite in the end of animation
                    self.kill()

            self.animation_curr_line += self.clock_frames

    def update(self):
        if self.is_exploded:
            self.exploded()
            return

        distance = self.get_distance_from_point()
        if distance > self.dfe_threshold:
            self.move_toward_point()

        self.fire()

    def __str__(self):
        return f"<Invader #{self.id}>"











