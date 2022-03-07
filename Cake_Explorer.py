from operator import index
from pygame import mixer
import pygame
import math
import random
import pickle
from pygame import mixer
from os import path

# initialize game engine
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps=60

window_width=1350
window_height=900

# Open a window
size = (window_width, window_height)
screen = pygame.display.set_mode(size)

#title and Icon
pygame.display.set_caption("Happy Birthday!")
icon=pygame.image.load('img/Grace_pic.png')
pygame.display.set_icon(icon)

#define game variable
tile_size = 50
game_over = 0
main_menu = True
background_select = 1
level = 1
max_levels = 6
key_num = 0

#Groups
robot_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()

#Text
over_font = pygame.font.Font('freesansbold.ttf',64)

#Load images
background_image1_1 = pygame.image.load('img/space_background.png')
background_image1= pygame.transform.scale(background_image1_1,(window_width, window_height))
background_image2 = pygame.image.load('img/github.png')
background_image2= pygame.transform.scale(background_image2,(window_width, window_height))
background_image3 = pygame.image.load('img/plains_background.png')
background_image3= pygame.transform.scale(background_image3,(window_width, window_height))
background_image4 = pygame.image.load('img/underwater_background.png')
background_image4= pygame.transform.scale(background_image4,(window_width, window_height))
background_image5 = pygame.image.load('img/Gothic_background.png')
background_image5= pygame.transform.scale(background_image5,(window_width, window_height))
background_image6 = pygame.image.load('img/Jungle_background.png')
background_image6= pygame.transform.scale(background_image6,(window_width, window_height))
background_image7 = pygame.image.load('img/asteroid_background.png')
background_image7= pygame.transform.scale(background_image7,(window_width, window_height))
background_image8 = pygame.image.load('img/ending.png')
background_image8= pygame.transform.scale(background_image8,(window_width, window_height))
restart_img = pygame.image.load('img/reset.png')
restart_img = pygame.transform.scale(restart_img,(100,50))
start_img = pygame.image.load('img/start_button.png')
start_img = pygame.transform.scale(start_img,(200,100))
exit_img = pygame.image.load('img/exit_button.png')
exit_img = pygame.transform.scale(exit_img,(200,100))

#Load sounds
pygame.mixer.music.load('img/background_music1.wav')
pygame.mixer.music.play(-1)
jump_fx = pygame.mixer.Sound('img/jump.wav')
jump_fx.set_volume(0.6)
lion_fx = pygame.mixer.Sound('img/lion.wav')
robot_fx = pygame.mixer.Sound('img/robot.wav')
lava_fx = pygame.mixer.Sound('img/lava.wav')
splat_fx = pygame.mixer.Sound('img/splat.wav')
portal_fx = pygame.mixer.Sound('img/portal.wav')
zoom_fx = pygame.mixer.Sound('img/zoom.wav')
zoom_fx.set_volume(0.2)
door_fx = pygame.mixer.Sound('img/door.wav')
door_fx.set_volume(0.5)
item_fx = pygame.mixer.Sound('img/item.wav')
item_fx.set_volume(0.6)
key_fx = pygame.mixer.Sound('img/key.wav')
ending_fx = pygame.mixer.Sound('img/ending.wav')

def reset_level(level):
    #function to reset level
    player.reset(100, window_height - 130)
    robot_group.empty()
    lava_group.empty()
    exit_group.empty()
    asteroid_group.empty()

    #Load in level data and create world
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)
    if level == 6:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('img\ending.wav'))
        pygame.mixer.music.stop()

    return world

def text():
    over_text = over_font.render("Collect the ingredients to continue.",True, (255,255,255))
    screen.blit(over_text,(140,250))

class Button ():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        screen.blit(self.image, self.rect)

        return action

class Player():
    def __init__(self,x,y):
        self.reset(x, y)

    def update(self, game_over,):
        #fliping image when flipping gravity
        if self.arrow_num == 0:
            self.images_left.clear()
            self.images_right.clear()
            for num in range(1,5):
                img_right = pygame.image.load(f'img/playa_walk{num}.png')
                img_right = pygame.transform.scale(img_right, (40,80))
                img_left = pygame.transform.flip(img_right, True, False)
                img_right = pygame.transform.flip(img_right, False, False)
                self.images_right.append(img_right)
                self.images_left.append(img_left)
        if self.arrow_num == 1:
            self.images_left.clear()
            self.images_right.clear()
            for num in range(1,5):
                img_right = pygame.image.load(f'img/playa_walk{num}.png')
                img_right = pygame.transform.scale(img_right, (40,80))
                img_left = pygame.transform.flip(img_right, True, True)
                img_right = pygame.transform.flip(img_right, False, True)
                self.images_right.append(img_right)
                self.images_left.append(img_left)
        dx = 0
        dy = 0
        walk_cooldown = 20
        if game_over == 0:
            #keypresses
            key = pygame.key.get_pressed()
            if self.arrow_num == 0:
                if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                    jump_fx.play()
                    self.vel_y = -8
                    self.jumped = True
                if key[pygame.K_SPACE] == False:
                    self.jumped = False
                    self.key_confirm = 1
                if key[pygame.K_LEFT]:
                    dx += -5
                    self.counter +=1
                    self.direction = -1
                if key[pygame.K_RIGHT]:
                    dx += 5
                    self.counter += 1
                    self.direction = 1
                if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                    self.counter = 0
                    self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]

            if self.arrow_num == 1:
                if key[pygame.K_SPACE] and self.jumped == False and self.in_air2 == False:
                    jump_fx.play()
                    self.vel_y = 8
                    self.jumped = True
                if key[pygame.K_SPACE] == False:
                    self.jumped = False
                    self.key_confirm = 1
                if key[pygame.K_LEFT]:
                    dx += -5
                    self.counter +=1
                    self.direction = -1
                if key[pygame.K_RIGHT]:
                    dx += 5
                    self.counter += 1
                    self.direction = 1
                if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                    self.counter = 0
                    self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]

            #add gravity
            if self.arrow_num == 0:
                self.vel_y += 0.3
                if self.vel_y > 5:
                    self.vel_y = 6
                dy += self.vel_y
            
            if self.arrow_num == 1:
                self.vel_y += -0.3
                if self.vel_y < -5:
                    self.vel_y = -6
                dy += self.vel_y


            #handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #key
            if level == 5:
                if key_num == 6:
                    self.i = 10
                    print("2")
                    for self.i in world.door_list:
                        door_fx.play()
                        del world.door_list[0]
            if level < 5:
                if key_num == 1:
                    self.i = 10
                    print("1")
                    for self.i in world.door_list:
                        door_fx.play()
                        del world.door_list[0]



            #ingredients
            self.ingredients_confirm = False
            for ingredients in world.ingredients_list:
                if ingredients[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    item_fx.play()
                    self.ingredients_confirm = True
                if self.ingredients_confirm == True:
                    del world.ingredients_list[0]
                    self.ingredients_confirm = False
                    

            #Arrow Gravity
            for arrow in world.arrowup_list:
                if arrow[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    zoom_fx.play()
                    self.arrow_num = 1
            for arrow in world.arrowdown_list:
                if arrow[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    zoom_fx.play()
                    self.arrow_num = 0

            #check for collision for Tiles
            self.in_air = True
            self.in_air2 = True
            for tile in world.tile_list:
                #check for collision for x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                        self.in_air2 = False
                    #check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #check for collision for Doors
            for tile in world.door_list:
                #check for collision for x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #check for collision with enemys
            if pygame.sprite.spritecollide(self, robot_group, False):
                if level == 2:
                    game_over = -1
                    robot_fx.play()
                if level == 4:
                    game_over = -1
                    lion_fx.play()
            
            #check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                lava_fx.play()

            #check for collision with asteroid
            if pygame.sprite.spritecollide(self, asteroid_group, False):
                game_over = -1
                splat_fx.play()

            #check for collision with exit
            if pygame.sprite.spritecollide(self, exit_group, False):
                if len(world.ingredients_list) == 0:
                    game_over = 1
                if len(world.ingredients_list) == 1:
                    text()

            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy
        elif game_over == -1:
            self.image = self.dead_image
            self.rect.y -= 4

            #Check if player has fallen off screen
        if self.rect.y <= -60:
            game_over = -1
        #draw player onto screen
        if level <= 5:
            screen.blit(self.image, self.rect)

        return game_over

    def reset (self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.arrow_num = 0
        if self.arrow_num == 0:
            for num in range(1,5):
                img_right = pygame.image.load(f'img/playa_walk{num}.png')
                img_right = pygame.transform.scale(img_right, (40,80))
                img_left = pygame.transform.flip(img_right, True, False)
                img_right = pygame.transform.flip(img_right, False, False)
                self.images_right.append(img_right)
                self.images_left.append(img_left)
        self.dead_image = pygame.image.load('img/angel.png')
        self.dead_image = pygame.transform.scale(self.dead_image, (80,80))
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

class World():
    def __init__(self,data):
        self.tile_list = []
        self.key_list = []
        self.door_list = []
        self.ingredients_list = []
        self.arrowup_list = []
        self.arrowdown_list = []

        #load images
        green_img = pygame.image.load('img/green.png')
        grey_img = pygame.image.load('img/grey.png')
        white_img = pygame.image.load('img/white.png')
        black_img = pygame.image.load('img/black.png')
        blue_img = pygame.image.load('img/blue.png')
        door_img = pygame.image.load('img/door.png')
        flour_img = pygame.image.load('img/flour.png')
        egg_img = pygame.image.load('img/egg.png')
        sugar_img = pygame.image.load('img/sugar.png')
        butter_img = pygame.image.load('img/butter.png')
        arrowup_img = pygame.image.load('img/arrowup.png')
        arrowdown_img = pygame.image.load('img/arrowdown.png')
        milk_img = pygame.image.load('img/milk.png')
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    #Green tile
                    img = pygame.transform.scale(green_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    #Grey tile
                    img = pygame.transform.scale(grey_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    #white tile
                    img = pygame.transform.scale(white_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    #black tile
                    img = pygame.transform.scale(black_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 5:
                    #blue tile
                    img = pygame.transform.scale(blue_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)                                              
                if tile == 6:
                    #Key
                    img = Key(col_count * tile_size, row_count * tile_size)
                    key_group.add(img)
                if tile == 7:
                    #Door
                    img = pygame.transform.scale(door_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.door_list.append(tile)
                if tile == 8:
                    #Flour
                    img = pygame.transform.scale(flour_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    ingredients = (img, img_rect)
                    self.ingredients_list.append(ingredients)
                if tile == 9:
                    #EGG
                    img = pygame.transform.scale(egg_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    ingredients = (img, img_rect)
                    self.ingredients_list.append(ingredients)
                if tile == 10:
                    #Sugar
                    img = pygame.transform.scale(sugar_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    ingredients = (img, img_rect)
                    self.ingredients_list.append(ingredients)
                if tile == 11:
                    #Butter
                    img = pygame.transform.scale(butter_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    ingredients = (img, img_rect)
                    self.ingredients_list.append(ingredients)
                if tile == 12:
                    #Arrow up
                    img = pygame.transform.scale(arrowup_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    arrow = (img, img_rect)
                    self.arrowup_list.append(arrow)
                if tile == 13:
                    #Arrow down
                    img = pygame.transform.scale(arrowdown_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    arrow = (img, img_rect)
                    self.arrowdown_list.append(arrow)
                if tile == 14:
                    #Robot
                    robot = Enemy(col_count * tile_size, row_count * tile_size + 5)
                    robot_group.add(robot)
                if tile == 15:
                    #Lava
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 16:
                    #Exit
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                if tile == 17:
                    #asteroid
                    asteroid = Asteroid(col_count * tile_size, row_count * tile_size)
                    asteroid_group.add(asteroid)
                if tile == 18:
                    #Butter
                    img = pygame.transform.scale(milk_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    ingredients = (img, img_rect)
                    self.ingredients_list.append(ingredients)


                col_count += 1
            row_count += 1
        
    def draw(self):
        for key in self.key_list:
            screen.blit(key[0], key[1])
        for ingredients in self.ingredients_list:
            screen.blit(ingredients[0], ingredients[1])
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
        for tile in self.door_list:
            screen.blit(tile[0], tile[1])        
        for arrow in self.arrowup_list:
            screen.blit(arrow[0], arrow[1])
        for arrow in self.arrowdown_list:
            screen.blit(arrow[0], arrow[1])

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        if level == 2:
            self.image = pygame.image.load('img/robot.png')
            self.image = pygame.transform.scale(self.image, (95,95))
        if level == 4:
            self.image = pygame.image.load('img/Tiger.png')
            self.image = pygame.transform.scale(self.image, (150,100))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.flag = 0
    
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if self.flag == 0:
            if self.move_direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)
                self.flag = 1
        if self.flag == 1:
            if self.move_direction == 1:
                self.image = pygame.transform.flip(self.image, True, False)
                self.flag = 0
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= -1

class Asteroid(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/asteroid.png')
        self.image = pygame.transform.scale(self.image, (95,95))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 6

    def update(self):
        self.rect.x += self.move_direction
        if self.rect.x >= 1350:
            self.move_direction = -6
        if self.rect.x <= -50:
            self.move_direction = 6

class Lava(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Key(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/key.png')
        img = pygame.transform.flip (img, True , False)
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(img, (tile_size * 1.2, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y




#Load in level data and create world
if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

player = Player(100, window_height - 130)

#create buttons
restart_button = Button(window_width // 2 - 50, window_height // 2 + 100, restart_img)
start_button = Button(window_width // 2 - 350, window_height // 2 + 250, start_img)
exit_button = Button(window_width // 2 + 150, window_height // 2 + 250, exit_img)
#Game Loop 
running = True
while running:
    clock.tick(fps)
    if background_select == 1:
        screen.blit(background_image2, (0,0))
    if background_select == 2:
        screen.blit(background_image3, (0,0))
    if background_select == 3:
        screen.blit(background_image4, (0,0))
    if background_select == 4:
        screen.blit(background_image5, (0,0))
    if background_select == 5:
        screen.blit(background_image6, (0,0))
    if background_select == 6:
        screen.blit(background_image7, (0,0))
    if background_select == 7:
        screen.blit(background_image8, (0,0))
    if main_menu == True:
        if exit_button.draw():
            running = False
        if start_button.draw():
            main_menu = False
            background_select += 1
    else:
        asteroid_group.draw(screen)
        world.draw()
        if game_over == 0:
            #check if key has been collected
            if pygame.sprite.spritecollide(player, key_group, True):
                key_num += 1
                key_fx.play()
            robot_group.update()
            asteroid_group.update()
        robot_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)
        key_group.draw(screen)

        game_over = player.update(game_over)

        #If player has died
        if game_over == -1:
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0
                key_num = 0
        
        #if player has completed the level
        if game_over == 1:
            #reset game and go to next level
            portal_fx.play()
            level += 1
            background_select += 1
            key_num = 0
            if level <= max_levels:
                #reset level
                world_data = []
                world = reset_level(level)
                game_over = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
pygame.quit()