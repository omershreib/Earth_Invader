import pygame
import math
from pygame.math import Vector2
from settings import *
from utilities import import_folder
from math import sin, cos
from random import randint
from functions import random_point, define_sprite_movement
import time


# to delete?
class GamePhysics:
    def __init__(self):
        self.low_orbit_range = (50,100)
        self.high_orbit_range = (100,200)
        self.low_angular_velocity = 5
        self.high_angular_velocity = 3

    def check_orbit(self, distance):
        if distance in self.low_orbit_range:
            return self.low_orbit_range

        if distance in self.high_orbit_range:
            return self.high_angular_velocity

        return 0


class Background(pygame.sprite.Sprite):
    def __init__(self, filepath):
        super().__init__()
        self.image = pygame.image.load(background_path)
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0


class Shell(pygame.sprite.Sprite):

    def __init__(self, cannon):
        super().__init__()

        self.image = pygame.Surface((16, 16))
        self.image.set_colorkey(COLOR_BLACK)
        pygame.draw.circle(self.image, COLOR_RED, (8, 8), 5)  # red ball
        self.rect = self.image.get_rect()
        self.velocity = 10
        self.radAngle = math.pi * cannon.angle / 180.

        barrelLen = cannon.cannonIm.get_width() / 2
        self.rect.center = \
            (cannon.pivot[0] + barrelLen * cos(self.radAngle),
             cannon.pivot[1] - barrelLen * sin(self.radAngle))

        #self.dest = (self.rect.centerx, self.rect.centery)

    def update(self):
        vel = self.velocity
        self.rect = self.rect.move(vel * cos(self.radAngle),
                                       -vel * sin(self.radAngle))


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
        self.image = pygame.image.load('../graphic/img/earth/Earth.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class InvaderBullets(pygame.sprite.Sprite):
    def __init__(self, invader_pos, target = EARTH_POSITION):
        super().__init__()

        # define ivader-bullet surface
        self.image = pygame.Surface((8, 8))
        self.image.set_colorkey(COLOR_BLACK)
        pygame.draw.circle(self.image, COLOR_LIME, (5,5), 2)
        self.rect = self.image.get_rect()

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

    def update(self):
        vel = self.velocity
        # self.x and self.y are floats, so the firing movement is more accurate
        # if converting them to an intagers
        self.x += int(self.dx)
        self.y += int(self.dy)

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.kill_sprite()

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def kill_sprite(self):
        if time.time() - self.time > self.time_to_kill:
            self.kill()


class InvaderBullets2(pygame.sprite.Sprite):
    def __init__(self, invader_pos, target = EARTH_POSITION):
        super().__init__()
        self.position = invader_pos
        self.target = target
        self.velocity = 2


        # define ivader-bullet surface
        self.image_size = (0, 0, 5, 5)
        self.image = pygame.Surface((8,8))
        self.image.set_colorkey(COLOR_BLACK)
        pygame.draw.ellipse(self.image, COLOR_LIME, self.image_size)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = invader_pos
        self.angle = 0
        self.fix_angle_to_target()

        # killing definitions
        self.time = time.time()
        self.time_to_kill = 5

    def fix_angle_to_target(self):
        y_diff = self.position[1] - self.target[1]
        x_diff = self.target[0] - self.position[0]
        self.angle = math.atan2(y_diff, x_diff) * 180. / math.pi

    def aim_bullet(self):
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()

    def update(self):
        vel = self.velocity
        angle = self.angle
        self.rect = self.rect.move(vel * cos(self.angle), -vel * sin(self.angle))  # fire
        #self.rect.centerx += vel*cos(angle)
        #self.rect.centery += vel*sin(angle)
        self.kill_sprite()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Invader(pygame.sprite.Sprite):
    def __init__(self, pos, id, screen):
        super().__init__()

        # generals
        image = pygame.image.load('../graphic/img/invaders/Invader01.png').convert_alpha()
        self.image = pygame.transform.smoothscale(image, invader_size).convert_alpha()
        self.oirign_img = self.image
        self.rect = self.image.get_rect(center=pos)
        #self.rect = self.image.get_rect(center=(1000,500))
        #self.pos = Vector2(pos)
        self.target_point = EARTH_POSITION
        self.id = id
        self.surface = screen


        # charactericstices
        self.health = 100
        self.fire_damage = 1
        self.velocity = 1
        self.vel_baseline = 3
        self.vel_curr_baseline = 0

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
        if self.fire_curr_baseline == self.fire_baseline:
            print(f"Invader {self} fire!")
            bullet = InvaderBullets(self.get_position())
            self.bullets.add(bullet)
            self.fire_curr_baseline = 0

        if self.fire_curr_baseline < self.fire_baseline:
            self.fire_curr_baseline += self.fire_loading_speed

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

    def update(self):
        distance = self.get_distance_from_point()
        if distance > self.dfe_threshold:
            self.move_toward_point()

        self.fire()

    def __str__(self):
        return f"<Invader #{self.id})>"















