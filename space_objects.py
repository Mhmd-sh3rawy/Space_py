"""
space_objects.py

Description:
    Defines core game elements and utility functions for the space shooter game.
    - Player: Represents the player-controlled spaceship.
    - Laser: Handles laser projectiles fired by the player.
    - Alien: Represents enemy units attacking the player.

    Additionally, this module provides:
    - Utility functions for loading images and keeping objects within screen bounds.

Authors:
    - Mohammed A. El-Sha3rawy
    - Ezzat

Date: 2025-03-26
License: N/A
"""

import pygame
from random import randint, uniform
from os import getcwd
from sys import exit

# functions to get images and audio files path
def img_path(filename):
    try:
        return f"images/{filename}"
    except FileExistsError:
        return f"{getcwd()}/images/{filename}"

def audio_path(filename):
    try:
        return f"audio/{filename}"
    except FileExistsError:
        return f"Final_Project/audio/{filename}"


# function for loading and scaling frames of the explosion
'''
def load_explosion_frames(frames_num:int, scale= 0.8):
    assert type(frames_num) == int
    frames = [pygame.image.load(img_path(f"Explosion4/{i:04d}.png")).convert_alpha() for i in range(1,frames_num+1)]
    #frames = [pygame.transform.scale_by(frames[j], scale) for j in range(frames_num)]
    return frames
'''
# function to keep pygame rectangles inside the screen
def stay_in_screen(rectangle):
    if rectangle.left < 0:
        rectangle.left = 0
    elif rectangle.right > 1024:
        rectangle.right = 1024
    if rectangle.top < 0:
        rectangle.top = 0
    elif rectangle.bottom > 720:
        rectangle.bottom = 720
    return rectangle


class Player(pygame.sprite.Sprite):
    def __init__(self, laser_surface , alien_group, laser_group ,groups):
        super().__init__(groups)
        self.image = pygame.image.load(img_path("spaceship.png")).convert_alpha()
        self.rect = self.image.get_rect(bottom = 720, centerx = 512)
        self.velocity = pygame.math.Vector2(0,0)
        self.all_sprites = groups
        self.alien_sprites = alien_group
        self.laser_sprites = laser_group
        self.laser_surface = laser_surface
        # cooldown attriputes
        self.shoot_time = 0
        self.shoot_enable = True
        self.cooldown_time = 200
        # health info
        self.health = 3

    
    # cool-down missile
    def cooldown_counter(self):
        if not self.shoot_enable:
            start_time = pygame.time.get_ticks()
            if start_time - self.shoot_time >= self.cooldown_time:
                self.shoot_enable = True
    
    # decrease the health by 1 if a collision occured
    def collision(self, alien):
        if pygame.sprite.spritecollide(self, alien, True):
            self.health -= 1

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        self.velocity.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.velocity.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        if self.velocity.magnitude() != 0:
            self.rect.center += self.velocity.normalize() * delta_time * 0.25
        if keys[pygame.K_SPACE] and self.shoot_enable:
            Laser(self.laser_surface,self.rect.midtop, (self.all_sprites, self.laser_sprites))
            self.shoot_enable = False
            self.shoot_time = pygame.time.get_ticks()
        self.collision(self.alien_sprites)
        self.cooldown_counter()
        stay_in_screen(self.rect)
    
class Laser(pygame.sprite.Sprite):
    def __init__(self,surface ,pos ,Groups):
        super().__init__(Groups)
        self.image = surface
        #pygame.transform.scale_by(self.image, 1) # This line will scale the laser image
        self.rect = self.image.get_rect(midtop = pos)
        
    def update(self, delta_time):
        self.rect.top -= 0.25 * delta_time
        if self.rect.bottom <= 0:
            self.kill()

class Alien(pygame.sprite.Sprite):
    def __init__(self, surf, health, laser_group , explosion_frames, Groups):
        super().__init__(Groups)
        image = surf
        self.image = pygame.transform.scale_by(image, 0.8)
        self.rect = self.image.get_rect(center = (randint(9,1024),randint(-90,0)))
        self.velocity = pygame.math.Vector2(uniform(-0.2,0.2),0.2)
        self.all_sprites = Groups
        self.laser_sprites = laser_group
        self.health = health + 1*(health == 0)
        self.dead = False
        self.explosion_frames = explosion_frames
    
    def get_damaged(self, laser_group):
        if self.health == 0:
            self.dead = True
        for laser in pygame.sprite.spritecollide(self,laser_group, True):
            self.health -= 1
            Explosion(self.explosion_frames, laser.rect.center, self.all_sprites)

    def update(self, delta_time):
        self.rect.center += self.velocity.normalize() * delta_time * 0.2
        self.get_damaged(self.laser_sprites)
        if self.rect.top > 720 or self.health == 0:
            self.kill()
        


class Explosion(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center = pos)
        self.current_time = pygame.time.get_ticks()

    def update(self, dt):
        if pygame.time.get_ticks() - self.current_time > 150:
            self.kill()

