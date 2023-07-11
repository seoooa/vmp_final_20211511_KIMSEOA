import pygame
import numpy as np
import os
import datetime

img_dir = os.path.join(os.path.dirname(__file__), 'img')
snd_dir = os.path.join(os.path.dirname(__file__), 'snd')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)

FPS = 60
l_on1 = False
l_on2 = True

b_on1 = False
b_on2 = False

msec_j2_1 = -1000000
msec_j1_1 = -1000000
sec_j2_1 = -1
sec_j1_1 = -1

score = 0

l1_snd_flag = 1
l2_snd_flag = 1
b1_snd_flag = 1
b2_snd_flag = 1

pygame.init()
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750
screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
pygame.display.set_caption('20211511 김서아')
 
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):

        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
 
class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    life = 3
 
    def __init__(self, x, y, who, dir):
        super().__init__()
 
        if who == 1:
            if dir == 1:
                self.image = pygame.transform.scale(player1_1_img, (21, 32))
            elif dir == 2:
                self.image = pygame.transform.scale(player1_2_img, (21, 32))
        if who == 2:
            if dir == 1:
               self.image = pygame.transform.scale(player2_1_img, (21, 32))
            elif dir == 2:
                self.image = pygame.transform.scale(player2_2_img, (21, 32))
 
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
 
    def changespeed(self, x, y):
        """ Change the speed of the player. Called with a keypress. """
        self.change_x += x
        self.change_y += y

    def jump(self,):
        self.change_y = -7
 
    def move(self, walls):
        # Move left/right
        self.rect.x += self.change_x

        wall_hit_list = pygame.sprite.spritecollide(self, walls, False)
        slider_hit_list = pygame.sprite.spritecollide(self,slider_list, False)

        for wall in wall_hit_list:
            if self.change_x > 0:
                self.rect.right = wall.rect.left
            else:
                self.rect.left = wall.rect.right

        for slider in slider_hit_list:
            if self.change_x > 0:
                self.rect.right = slider.rect.left
            else:
                self.rect.left = slider.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        wall_hit_list = pygame.sprite.spritecollide(self, walls, False)
        slider_hit_list = pygame.sprite.spritecollide(self, slider_list, False)

        if wall_hit_list == []:
            for i in range(10):
                self.change_y += 0.03

        for wall in wall_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = wall.rect.top
            elif self.change_y < 0:
                self.rect.top = wall.rect.bottom
                self.change_y = 0.03
        
        for slider in slider_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y >= 0:
                self.rect.bottom = slider.rect.top
                self.change_y = 0
            elif self.change_y < 0:
                self.rect.top = slider.rect.bottom 
                self.change_y = 0.03

 
class Room(object):
    """ Base class for all rooms. """
    wall_list = None
    enemy_sprites = None
 
    def __init__(self):
        """ Constructor, create our lists. """
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

class Obs(object):
    blue_list = None
    red_list = None
    green_list = None
    lever_list = None
    slider_list = None
    coin_list = None

    def __init__(self):
        self.blue_list = pygame.sprite.Group()
        self.red_list = pygame.sprite.Group()
        self.green_list = pygame.sprite.Group()
        self.lever_list = pygame.sprite.Group()
        self.slider_list = pygame.sprite.Group()
        self.coin_list = pygame.sprite.Group()

class Room1(Room):
    def __init__(self):
        super().__init__()

        walls = [[0, 0, 20, 750, WHITE],
                 [1180, 0, 20, 750, WHITE],
                 [0, 0, 1200, 80, WHITE],
                 [20, 210, 1010, 20, WHITE],
                 [170, 340, 1030, 20, WHITE],
                 [20, 470, 700, 20, WHITE],
                 [750, 530, 100, 20, WHITE],
                 [850, 600, 100, 20, WHITE],
                 [20, 600, 300, 20, WHITE],
                 [1000, 650, 200, 20, WHITE],
                 [20, 730, 1200, 20, WHITE]
                ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)
 
class Greenwall(Obs):
    def __init__(self,):
        super().__init__()

        green_walls = [[350, 720, 300, 20, GREEN],
                 [600, 330, 130, 20, GREEN]]
        
        for item in green_walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            if item == green_walls[0]:
                wall.image = pygame.transform.scale(greenwall2_img, (300, 30))
            else:
                wall.image = pygame.transform.scale(greenwall1_img, (120, 30))
            wall.image.set_colorkey(BLACK)
            wall.rect = wall.image.get_rect()
            wall.rect.x = item[0]
            wall.rect.y = item[1]
            
            self.green_list.add(wall)

class Redwall(Obs):
    def __init__(self,):
        super().__init__()

        fire_walls = [[800, 720, 120, 30, RED],
                 [800, 330, 120, 30, RED]]
        
        for item in fire_walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            wall.image = pygame.transform.scale(redwall1_img, (120, 30))
            wall.image.set_colorkey(BLACK)
            wall.rect = wall.image.get_rect()
            wall.rect.x = item[0]
            wall.rect.y = item[1]
            
            self.red_list.add(wall)

class BlueWall(Obs):
    def __init__(self,):
        super().__init__()

        blue_walls = [[450, 460, 120, 30, BLUE]]
        
        for item in blue_walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            wall.image = pygame.transform.scale(bluewall1_img, (120, 30))
            wall.image.set_colorkey(BLACK)
            wall.rect = wall.image.get_rect()
            wall.rect.x = item[0]
            wall.rect.y = item[1]
            
            self.blue_list.add(wall)

class Lever():
    def __init__(self, x, y, width, height, on):
        self.lever = pygame.sprite.Group()

        lever = [[x, y, width, height, YELLOW]]
        
        for item in lever:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            if on == True:
                wall.image = pygame.transform.scale(lever2_img, (20, 40))
            else:
                wall.image = pygame.transform.scale(lever1_img, (20, 40))
            wall.image.set_colorkey(BLACK)
            wall.rect = wall.image.get_rect()
            wall.rect.x = item[0]
            wall.rect.y = item[1]

            self.lever.add(wall)

class Button():
    def __init__(self, x, y, width, height, on):
        self.button = pygame.sprite.Group()

        button = [[x, y, width, height, PURPLE]]
        
        for item in button:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])

            if on == True:
                wall.image = pygame.transform.scale(button2_img, (20, 30))
            else:
                wall.image = pygame.transform.scale(button1_img, (20, 30))

            wall.image.set_colorkey(BLACK)
            wall.rect = wall.image.get_rect()
            wall.rect.x = item[0]
            wall.rect.y = item[1]
            self.button.add(wall)

class Flag():
    def __init__(self, x, y, width, height, who):
        self.flag = pygame.sprite.Group()

        flag = [[x, y, width, height, WHITE]]
        
        for item in flag:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])

            if who == 1:
                wall.image = pygame.transform.scale(Mflag_img, (30, 100))
            elif who == 2:
                wall.image = pygame.transform.scale(Lflag_img, (30, 100))

            wall.image.set_colorkey(BLACK)
            wall.rect = wall.image.get_rect()
            wall.rect.x = item[0]
            wall.rect.y = item[1]

            self.flag.add(wall)

class Coin(Obs):
    def __init__(self,):
        super().__init__()

        coin = [[500, 650, 24, 32, YELLOW],
                [1100, 550, 24, 32, YELLOW],
                [500, 380, 24, 32, YELLOW],
                [800, 450, 24, 32, YELLOW],
                [100, 250, 24, 32, YELLOW],
                [500, 120, 24, 32, YELLOW],
                [530, 120, 24, 32, YELLOW],
                [560, 120, 24, 32, YELLOW],
                [590, 120, 24, 32, YELLOW],
                [620, 120, 24, 32, YELLOW]]
        
        for item in coin:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            wall.image = pygame.transform.scale(coin_img, (24, 32))
            wall.image.set_colorkey(BLACK)
            wall.rect = wall.image.get_rect()
            wall.rect.x = item[0]
            wall.rect.y = item[1]
            
            self.coin_list.add(wall)

class Slider(pygame.sprite.Sprite):

    change_y = 0
    start_Flag = 0

    def __init__(self, x, y, width, height):
        super().__init__()
        self.x_pos = x
        self.y_pos = y

        self.image = pygame.transform.scale(slider_img, (150, 25))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def changespeed(self, y, where):
        if self.rect.y < where:
            self.change_y += y 
        elif y < 0:
            self.change_y += y 
    
    def move(self, where):
        self.rect.y += self.change_y

        if self.rect.y == where:
            self.change_y = 0

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img = pygame.transform.scale(img, (30, 40))
        img_rect = img.get_rect()
        img.set_colorkey(BLACK)
        img_rect.x = x + 40 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font('dalmoori.ttf', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def show_start_screen():
    background_snd.play(-1)
    screen.blit(startscreen, startscreen_rect)
    screen.blit(title_img, (WINDOW_WIDTH/3, 50))
    draw_text(screen, "If you want to Start, Press any keys", 20, WINDOW_WIDTH / 2, 400 , WHITE)
    draw_text(screen, "Player 1 : a, w, s key", 20, 150, 200 , WHITE)
    draw_text(screen, "Player 2 : direction key", 20, 160, 250 , WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_clear_screen(min, sec):
    background_snd.stop()
    start_snd.play()
    clear_snd.play()

    screen.blit(startscreen, startscreen_rect)
    draw_text(screen, "Clear!", 70, WINDOW_WIDTH / 2, 120 , WHITE)
    draw_text(screen, "Your Record is " + str(min) + ': ' + str(sec), 40, WINDOW_WIDTH / 2, 230 , WHITE)
    draw_text(screen, "Score :", 30, WINDOW_WIDTH / 2 - 80, 290, WHITE)
    screen.blit(coin_img, (WINDOW_WIDTH / 2, 290))
    draw_text(screen, ' X ' + str(score), 30, WINDOW_WIDTH/2 + 70, 290, WHITE)
    pygame.display.flip()

    Rank()
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def show_gameover_screen():
    background_snd.stop()
    gameover_snd.play()
    screen.blit(startscreen, startscreen_rect)
    draw_text(screen, "GAME OVER", 100, WINDOW_WIDTH / 2, 200 , WHITE)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def Rank():
    user_name = input("Enter Your Name: ")

    f_r = open("rank.txt", 'r')
    sort_rank = []
    read_num = int(f_r.readline())

    for i in range(read_num):
        readrank = f_r.readline()
        readrank = readrank.split(' ')
        sort_rank.append(readrank)
    f_r.close()

    readrank = [user_name, timer_min, timer_sec, score]
    sort_rank.append(readrank)
    read_num += 1
    
    for i in range(read_num):
        if len(sort_rank) == 1:
            break

        for j in range(i) :
            if int(sort_rank[i][1]) < int(sort_rank[j][1]) or (int(sort_rank[i][1]) == int(sort_rank[j][1]) and int(sort_rank[i][2]) < int(sort_rank[j][2])) or (int(sort_rank[i][1]) == int(sort_rank[j][1]) and int(sort_rank[i][2]) == int(sort_rank[j][2]) and int(sort_rank[i][3]) > int(sort_rank[j][3])):
                temp = sort_rank[i] 
                sort_rank[i] = sort_rank[j]
                sort_rank[j] = temp

    f_w = open("rank.txt", 'w')
    f_w.write('%d\n' %read_num)
    for i in range(read_num):
        f_w.write("%s %s %s %s \n" %(sort_rank[i][0], sort_rank[i][1], sort_rank[i][2], sort_rank[i][3]))
    
    f_w.close()

    print("Good Job!")
    draw_text(screen, 'TOP 5:', 20, WINDOW_WIDTH/2 - 210, 350, BLACK)
    draw_text(screen, 'Name         Record      Score', 20, WINDOW_WIDTH/2, 350, BLACK)

    if read_num > 5:
        read_num = 5
    for i in range(read_num):
        draw_text(screen, sort_rank[i][0], 20, WINDOW_WIDTH/2 - 130, 390 + i * 22, BLACK)
        draw_text(screen, str(sort_rank[i][1]), 20, WINDOW_WIDTH/2 - 10, 390 + i * 22, BLACK)
        draw_text(screen, ' : ', 20, WINDOW_WIDTH/2 + 10, 390 + i * 20, BLACK)
        draw_text(screen, str(sort_rank[i][2]), 20, WINDOW_WIDTH/2 + 30, 390 + i * 22, BLACK)
        draw_text(screen, str(sort_rank[i][3]), 20, WINDOW_WIDTH/2 + 120, 390 + i * 22, BLACK)

""" Main Program """

#Load All Images
background = pygame.image.load(os.path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()
startscreen = pygame.image.load(os.path.join(img_dir, "startscreen.png")).convert()
startscreen_rect = background.get_rect()
title_img = pygame.image.load(os.path.join(img_dir, "logo.png")).convert()
title_img =  pygame.transform.scale(title_img, (400, 320))
player1_1_img = pygame.image.load(os.path.join(img_dir, "player1_1.png")).convert()
player2_1_img = pygame.image.load(os.path.join(img_dir, "player2_1.png")).convert()
player1_2_img = pygame.image.load(os.path.join(img_dir, "player1_2.png")).convert()
player2_2_img = pygame.image.load(os.path.join(img_dir, "player2_2.png")).convert()
player1_mini_img = pygame.image.load(os.path.join(img_dir, "player1_mini.png")).convert()
player2_mini_img = pygame.image.load(os.path.join(img_dir, "player2_mini.png")).convert()
slider_img = pygame.image.load(os.path.join(img_dir, "slider.png")).convert()
redwall1_img = pygame.image.load(os.path.join(img_dir, "redwall.png")).convert()
greenwall1_img = pygame.image.load(os.path.join(img_dir, "greenwall_1.png")).convert()
greenwall2_img = pygame.image.load(os.path.join(img_dir, "greenwall_2.png")).convert()
bluewall1_img = pygame.image.load(os.path.join(img_dir, "bluewall.png")).convert()
button1_img = pygame.image.load(os.path.join(img_dir, "button1.png")).convert()
button2_img = pygame.image.load(os.path.join(img_dir, "button2.png")).convert()
lever1_img = pygame.image.load(os.path.join(img_dir, "lever1.png")).convert()
lever2_img = pygame.image.load(os.path.join(img_dir, "lever2.png")).convert()
Mflag_img = pygame.image.load(os.path.join(img_dir, "M_flag.png")).convert()
Lflag_img = pygame.image.load(os.path.join(img_dir, "L_flag.png")).convert()
respawn_img = pygame.image.load(os.path.join(img_dir, "respawn.png")).convert()
respawn_img.set_colorkey(BLACK)
coin_img = pygame.image.load(os.path.join(img_dir, "coin.png")).convert()
coin_img.set_colorkey(BLACK)

#Load All Sounds
start_snd = pygame.mixer.Sound(os.path.join(snd_dir, 'start.mp3'))
background_snd = pygame.mixer.Sound(os.path.join(snd_dir, 'supermario.mp3'))
coin_snd = pygame.mixer.Sound(os.path.join(snd_dir, 'coin.mp3'))
jump_snd = pygame.mixer.Sound(os.path.join(snd_dir, 'jump.mp3'))
clear_snd = pygame.mixer.Sound(os.path.join(snd_dir, 'clear.mp3'))
rewspawn_snd = pygame.mixer.Sound(os.path.join(snd_dir, 'respawn.wav'))
push_snd = pygame.mixer.Sound(os.path.join(snd_dir, 'push.wav'))
gameover_snd = pygame.mixer.Sound(os.path.join(snd_dir, 'gameover.wav'))
pygame.mixer.music.set_volume(0.1)

player1 = Player(100, 650, 1, 1)
player2 = Player(100, 520, 2, 1)

slider_list = pygame.sprite.Group()
slider1 = Slider(20, 340, 150, 25)
slider2 = Slider(1030, 210, 150, 25)
slider_list.add(slider1)
slider_list.add(slider2)

movingsprites = pygame.sprite.Group()
movingsprites.add(player1)
movingsprites.add(player2)
movingsprites.add(slider1)
movingsprites.add(slider2)

obs1 = Greenwall()
obs2 = Redwall()
obs3 = BlueWall()
obs4 = Coin()

lever1 = Lever(720, 710, 20, 40, l_on1)
lever2 = Lever(300, 450, 20, 40, l_on2)

button1 = Button(300, 330, 20, 30, b_on1)
button2 = Button(900, 200, 20, 30, b_on2)

flag1 = Flag(100, 110, 30, 100, 1)
flag2 = Flag(200, 110, 30, 100, 2)

rooms = []
 
room = Room1()
rooms.append(room)

current_room_no = 0
current_room = rooms[current_room_no]
 
clock = pygame.time.Clock()
 
first_flag = 0
s2_ypos = 270

GameOver = False
GameStart = True
while not GameOver:
    
    if GameStart == True:
        show_start_screen()
        Start = datetime.datetime.now()

        min_s = Start.minute
        sec_s = Start.second

        GameStart = False

    Now = datetime.datetime.now()
    min_n = Now.minute
    sec_n = Now.second

    timer_min = min_n - min_s
    timer_sec = sec_n - sec_s

    if timer_sec < 0:
        timer_min -= 1
        timer_sec += 60

    if timer_min < 0:
        timer_min += 60

    timer_sec = timer_sec + timer_min * 60
    timer_min = int(timer_sec / 60)
    timer_sec -= int(timer_min) * 60

    # --- Event Processing ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameOver = True
 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player2.__init__(player2.rect.x, player2.rect.y, 2, 2)
                player2.changespeed(-4, 0)
            if event.key == pygame.K_RIGHT:
                player2.__init__(player2.rect.x, player2.rect.y, 2, 1)
                player2.changespeed(4, 0)
            if event.key == pygame.K_UP:
                Jump2 = datetime.datetime.now()
                sec_j2_2 = Jump2.second
                msec_j2_2 = Jump2.microsecond

                jump_stime2 = sec_j2_2 - sec_j2_1
                jump_mtime2 = msec_j2_2 - msec_j2_1

                if jump_stime2 < 0:
                    jump_stime2 += 60

                if jump_stime2 >= 1 and jump_mtime2 < 0:
                    jump_mtime2 += 1000000

                if jump_mtime2 >= 700000 or (jump_stime2 == 1 and 1000000 - jump_mtime2 > 700000) or jump_stime2 > 1:
                    jump_snd.play()
                    player2.jump()
                    sec_j2_1 = sec_j2_2
                    msec_j2_1 = msec_j2_2

            if event.key == pygame.K_a:
                player1.__init__(player1.rect.x, player1.rect.y, 1, 2)
                player1.changespeed(-4, 0)
            if event.key == pygame.K_d:
                player1.__init__(player1.rect.x, player1.rect.y, 1, 1)
                player1.changespeed(4, 0)
            if event.key == pygame.K_w:
                Jump1 = datetime.datetime.now()
                sec_j1_2 = Jump1.second
                msec_j1_2 = Jump1.microsecond

                jump_stime1 = sec_j1_2 - sec_j1_1
                jump_mtime1 = msec_j1_2 - msec_j1_1

                if jump_stime1 < 0:
                    jump_stime1 += 60

                if jump_stime1 >= 1 and jump_mtime1 < 0:
                    jump_mtime1 += 1000000

                if jump_mtime1 >= 700000 or (jump_stime1 == 1 and 1000000 - jump_mtime1 > 700000) or jump_stime1 > 1:
                    jump_snd.play()
                    player1.jump()
                    sec_j1_1 = sec_j1_2
                    msec_j1_1 = msec_j1_2   
 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player2.changespeed(4, 0)
            if event.key == pygame.K_RIGHT:
                player2.changespeed(-4, 0)

            if event.key == pygame.K_a:
                player1.changespeed(4, 0)
            if event.key == pygame.K_d:
                player1.changespeed(-4, 0)

    # --- Game Logic ---
    player1.move(current_room.wall_list)
    player2.move(current_room.wall_list)
    slider1.move(400)
    slider2.move(s2_ypos)
 
    if player2.rect.x < -15:
        if current_room_no == 0:
            current_room_no = 2
            current_room = rooms[current_room_no]
            player2.rect.x = 790
        elif current_room_no == 2:
            current_room_no = 1
            current_room = rooms[current_room_no]
            player2.rect.x = 790
        else:
            current_room_no = 0
            current_room = rooms[current_room_no]
            player2.rect.x = 790
 
    if player2.rect.x > 2001:
        if current_room_no == 0:
            current_room_no = 1
            current_room = rooms[current_room_no]
            player2.rect.x = 0
        elif current_room_no == 1:
            current_room_no = 2
            current_room = rooms[current_room_no]
            player2.rect.x = 0
        else:
            current_room_no = 0
            current_room = rooms[current_room_no]
            player2.rect.x = 0
 
    if pygame.sprite.spritecollide(player1, obs1.green_list, False) or pygame.sprite.spritecollide(player1, obs3.blue_list, False):
        player1.rect.x = 100
        player1.rect.y = 650

        player1.life -= 1
        if player1.life == 0:
            show_gameover_screen()
            GameOver = True

        rewspawn_snd.play()

    if pygame.sprite.spritecollide(player2, obs2.red_list, False) or pygame.sprite.spritecollide(player2, obs3.blue_list, False):
        player2.rect.x = 100
        player2.rect.y = 520

        player2.life -= 1
        if player2.life == 0:
            show_gameover_screen()
            GameOver = True
        
        rewspawn_snd.play()

    if pygame.sprite.spritecollide(player1, obs4.coin_list, True) or pygame.sprite.spritecollide(player2, obs4.coin_list, True):
        coin_snd.play()
        score += 1

    if pygame.sprite.spritecollide(player1, flag1.flag, False) and pygame.sprite.spritecollide(player2, flag2.flag, False):
        show_clear_screen(timer_min, timer_sec)
        pygame.display.flip()
        GameOver = True

    if pygame.sprite.spritecollide(player1, lever1.lever, False) or pygame.sprite.spritecollide(player2, lever1.lever, False):
        if l1_snd_flag == 1:
            push_snd.play()
            l1_snd_flag = 0

        l_on1 = True
        lever1.__init__(720, 710, 20, 40, l_on1)
        for water in obs1.green_list:
            if first_flag == 0:
                obs1.green_list.remove(water)
                first_flag = 1

    if pygame.sprite.spritecollide(player1, lever2.lever, False) or pygame.sprite.spritecollide(player2, lever2.lever, False):
        if l2_snd_flag == 1:
            push_snd.play()
            l2_snd_flag = 0

        l_on2 = False
        lever2.__init__(300, 450, 20, 40, l_on2)
        for i in range(60):
            slider1.changespeed(0.1, 400)
        slider1.start_Flag = 0

    if pygame.sprite.spritecollide(player1, button1.button, False) or pygame.sprite.spritecollide(player2, button1.button, False) or pygame.sprite.spritecollide(player1, button2.button, False) or pygame.sprite.spritecollide(player2, button2.button, False):

        if pygame.sprite.spritecollide(player1, button1.button, False) or pygame.sprite.spritecollide(player2, button1.button, False):
            if b1_snd_flag == 1:
                push_snd.play()
                b1_snd_flag = 0
            b_on1 = True
            button1.__init__(300, 330, 20, 30, b_on1)

        if pygame.sprite.spritecollide(player1, button2.button, False) or pygame.sprite.spritecollide(player2, button2.button, False):
            if b2_snd_flag == 1:
                push_snd.play()
                b2_snd_flag = 0
            b_on2 = True
            button2.__init__(900, 200, 20, 30, b_on2)

        s2_ypos = 270
        slider2.start_Flag = 1
        for i in range(60):
            slider2.changespeed(0.1, 270)

    elif slider2.start_Flag == 1 and not pygame.sprite.spritecollide(player1, button1.button, False) and not pygame.sprite.spritecollide(player2, button1.button, False) and not pygame.sprite.spritecollide(player1, button2.button, False) and not pygame.sprite.spritecollide(player2, button2.button, False):
        
        if not pygame.sprite.spritecollide(player1, button1.button, False) and not pygame.sprite.spritecollide(player2, button1.button, False):
            b_on1 = False
            b1_snd_flag = 1
            button1.__init__(300, 330, 20, 30, b_on1)
        if not pygame.sprite.spritecollide(player1, button2.button, False) and not pygame.sprite.spritecollide(player2, button2.button, False):
            b_on2 = False
            b2_snd_flag = 1
            button2.__init__(900, 200, 20, 30, b_on2)

        s2_ypos = 210
        for i in range(60):
            slider2.changespeed(-0.1, 210)
        slider2.start_Flag = 0

    # --- Drawing ---
    screen.fill(BLACK)
    current_room.wall_list.draw(screen)
    screen.blit(background, background_rect)
    screen.blit(respawn_img, (20, 650))
    screen.blit(respawn_img, (20, 520))

    screen.blit(coin_img, (WINDOW_WIDTH/2 + 150, 25))
    draw_text(screen, ' X ' + str(score), 30, WINDOW_WIDTH/2 + 200, 25, WHITE)

    draw_lives(screen, 25, 20, player1.life, player1_mini_img)
    draw_lives(screen, WINDOW_WIDTH - 135, 20, player2.life, player2_mini_img)
    draw_text(screen, 'player 1', 25, 200, 30, WHITE)
    draw_text(screen, 'player 2', 25, WINDOW_WIDTH - 200, 30, WHITE)
    draw_text(screen, str(timer_min) + ':', 50, WINDOW_WIDTH/2 - 20, 25, WHITE)
    draw_text(screen, str(timer_sec), 50, WINDOW_WIDTH/2 + 30, 25, WHITE)

    obs1.green_list.draw(screen)
    obs2.red_list.draw(screen)
    obs3.blue_list.draw(screen)
    lever1.lever.draw(screen)
    lever2.lever.draw(screen)
    button1.button.draw(screen)
    button2.button.draw(screen)
    flag1.flag.draw(screen)
    flag2.flag.draw(screen)
    obs4.coin_list.draw(screen)
    movingsprites.draw(screen)

    pygame.display.flip()
 
    clock.tick(60)
 
pygame.quit()
