import pygame
import time
from pygame.locals import *
import random

pygame.init()

# craete the screen
game_width = 800
game_height = 600
screen_size = (game_width, game_height)
pygame_window = pygame.display.set_mode(screen_size)
pygame.display.set_caption("space_shooter_game")

# set the color
red = (200, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

# deefine the font
font20 = pygame.font.SysFont("Constantia", 20)
font30 = pygame.font.SysFont("Constantia", 30)
font40 = pygame.font.SysFont("Constantia", 40)
font10 = pygame.font.SysFont("Constantia", 10)
font50 = pygame.font.SysFont("Constantia", 50)


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.lives = 3
        self.score = 0

        # load spaceship image
        image = pygame.image.load("spaceship.png")
        image_scale = 40 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        scaled_size = (new_width, new_height)
        self.image = pygame.transform.scale(image, scaled_size)
        self.rect = self.image.get_rect()

        # dispalying damage
        self.invincibility_frame = 0
        damage_image = pygame.image.load("exp2.png")
        image_scale = 80 / damage_image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        scaled_size = (new_width, new_height)
        self.damage_image = pygame.transform.scale(damage_image, scaled_size)

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

        if self.invincibility_frame > 0:
            self.invincibility_frame -= 1

    def draw_damage(self):
        if self.invincibility_frame > 0:
            damage_x = self.x - self.image.get_width() / 3
            damage_y = self.y - self.image.get_height() / 3
            pygame_window.blit(self.damage_image, (damage_x, damage_y))


class meteor(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.hits = 1
        self.points = 1
        # randome color, size , number of  meteor
        num = random.randint(1, 5)
        self.image = pygame.image.load(f"alien{num}.png")

        # set number of hit require to destroy the meteor
        # the point added to score if the meteor is destroyed
        if num == 4:
            self.hits = 5
            self.points = 5
        elif num == 3:
            self.hits = 4
            self.points = 4
        elif num == 2:
            self.hits = 2
            self.points = 2
        elif num == 1:
            self.hits = 3
            self.points = 3
        elif num == 5:
            self.hits = 1
            self.points = 1
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        # move the meteor down
        self.rect.y += 1

        # rorate the meteor
        #  if self.rect.y % 20 ==0 :
        #      self.image = pygame.transform.rotate(self.image, 90)

        # check for collision with the player
        if pygame.sprite.spritecollide(self, player_group, False):
            self.kill()
            # 1 decreas player life if the meteor hit the player
            if player.invincibility_frame == 0:
                player.lives -= 1

                # 2 display the damage image for 50 frame

                player.invincibility_frame = 50

        # check for collision with the missile
        if pygame.sprite.spritecollide(self, missile_group, True):
            self.hits -= 1
            # 1 add score point if the meteor is destroyed
            if self.hits == 0:
                player.score += self.points

                # remove the meteor if it is out of the screen or destroyed
        if self.rect.top > game_height or self.hits == 0:
            self.kill()


class Missile(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 4, 8)

    def draw(self):
        for w in range(self.rect.width):
            for h in range(self.rect.height):
                pygame_window.set_at((self.rect.x + w, self.rect.y - h), white)

    def update(self):

        # missile movement
        self.rect.y -= 5
        # display the missile
        if self.rect.bottom > 0:
            self.draw()
        else:
            self.kill()


# creat a sprite group
player_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()

# load the image of bckground
bg = pygame.image.load("bg.png")

# craete the player object
player_x = 377
player_y = 500
player = Player(player_x, player_y)
player_group.add(player)

# missile coldwon timer
missile_cooldown = 200
last_missile = pygame.time.get_ticks() - missile_cooldown

# define the count down timer
count_down = 3
last_count = pygame.time.get_ticks()

# define the gameover condition
# 0 is no game over 1 is mean won , -1 is mean lose
game_over = 0


#  creat a new meteor
def create_meteor():
    meteor_x = random.randint(0, game_width - 50)
    meteor_y = 0
    new_meteor = meteor(meteor_x, meteor_y)
    meteor_group.add(new_meteor)


create_meteor()


# define a function for creat the text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    pygame_window.blit(img, (x, y))


draw_text("", font40, white, 300, 200)

# game loop
clock = pygame.time.Clock()
running = True
fps = 120
loop_ctr = 0
# !##############################################
while running:
    loop_ctr += 1

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # move the player
    if keys[K_LEFT] and player.rect.left > 0:
        player.x -= 5
    elif keys[K_RIGHT] and player.rect.right < game_width:
        player.x += 5

        # fire the missile with space bar

    if keys[K_SPACE]:
        current_time = pygame.time.get_ticks()
        if current_time - last_missile > missile_cooldown:
            missile = Missile(player.rect.centerx, player.rect.top)
            missile_group.add(missile)
            last_missile = current_time

            # draw the background

    for bg_x in range(0, game_width, bg.get_width()):
        for bg_y in range(0, game_height, bg.get_height()):
            pygame_window.blit(bg, (bg_x, bg_y))

        if count_down > 0:
            draw_text('GET RAEDY!', font40, white, int(game_width / 2 - 110), int(game_height / 2 + 50))
            draw_text(str(count_down), font40, white, int(game_width / 2 - 10), int(game_height / 2 + 100))
            count_timer = pygame.time.get_ticks()
            if count_timer - last_count > 1000:
                count_down -= 1
                last_count = count_timer

            #  screen drawing and ubdates
    player_group.draw(pygame_window)
    player.draw_damage()
    player_group.update()
    # create a new meteor every 75 frame
    if loop_ctr == 75:
        create_meteor()
        loop_ctr = 0

    # the loop after get game over
    if game_over == -1:
        player_group.empty()
        meteor_group.empty()
        missile_group.empty()
        draw_text("GAME OVER!", font50, red, 250, 250)
        pygame.display.update()
        time.sleep(3)
        game_over = 0
        player.lives = 3
        player.score = 0
        create_meteor()
        player_x = 377
        player_y = 500
        player = Player(player_x, player_y)
        player_group.add(player)
        missile_group.empty()
        meteor_group.empty()
        count_down = 3
        last_count = pygame.time.get_ticks()

    #  screen darawing ubdates show after count get 0

    # start all moves after count down = 0
    if count_down == 0:
        missile_group.update()
        meteor_group.update()
        meteor_group.draw(pygame_window)

    # draw the score and the lives
    draw_text("LIVES: " + str(player.lives), font20, blue, 7, 5)
    draw_text("SCORE: " + str(player.score), font20, blue, 7, 25)
    # make game over after lives get 0
    if player.lives == 0:
        game_over = -1

    pygame.display.update()

pygame.quit()



