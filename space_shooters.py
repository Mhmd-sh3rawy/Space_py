from random import randint
#custom module providing all objects for the game
from space_objects import  *
""" Contains required objects and procedures for making games """
import pygame


# intitializing the screen
screen = pygame.display.set_mode((1024,720))
pygame.init()

# background and multible surface sprites
background = pygame.image.load(img_path("Space Background.png")).convert_alpha()
background_rect = background.get_rect(top = 0)
laser_surf = pygame.image.load(img_path("missile (2).png")).convert_alpha()
aliens = [pygame.image.load(img_path(f"alien{i}.png")).convert_alpha() for i in range(1,5)]



# all instances of the game classes
all_sprites = pygame.sprite.Group()
Aliens_sprites = pygame.sprite.Group()
Laser_sprites = pygame.sprite.Group()
spaceship = Player(laser_surf,Aliens_sprites, Laser_sprites,  all_sprites)  

explosion_frames = [pygame.image.load(img_path(f"Explosion4/{i:04d}.png")).convert_alpha() for i in range(1,22)]
frame_index = 0

# Timers and generate aliens event 
clock = pygame.time.Clock()
generate_aliens = pygame.event.custom_type()
pygame.time.set_timer(generate_aliens, 500)

# Timers and event for moving explosion frames
move_frames = pygame.event.custom_type()
pygame.time.set_timer(move_frames, 10)

# The main game loop
RUNNING = True
keys = pygame.key.get_pressed()
while RUNNING:
    if spaceship.health == 0:
        pygame.quit()
        exit()
    else:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == generate_aliens:
                x = randint(0,3)
                object_alien = Alien(aliens[x], x, Laser_sprites , explosion_frames[frame_index] ,(all_sprites,Aliens_sprites))
            if event.type == move_frames:
                frame_index = (frame_index + 1)%21
    
        screen.blit(background, background_rect)
        all_sprites.update(dt)
        all_sprites.draw(screen)
        pygame.display.update()


