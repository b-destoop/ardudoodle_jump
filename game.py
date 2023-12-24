import time
from typing import Any
import pygame
from pygame.locals import *
import sys
import random
import serial

arduino = serial.Serial(port='COM5', baudrate=9600, timeout=2) 
 
pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        #self.image = pygame.image.load("character.png")
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255,255,0))
        self.rect = self.surf.get_rect()
   
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
 
    def move(self):
        self.acc = vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
                 
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
             
        self.rect.midbottom = self.pos
 
    def jump(self): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15
 
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
 
    def update(self):
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:               
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
                    self.jump()
 
 
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10),
                                                 random.randint(0, HEIGHT-30)))
        
        self.speed = random.randint(-1, 1)
        self.moving = bool(random.getrandbits(1))
 
    def move(self):
        if self.moving == True:  
            self.rect.move_ip(self.speed,0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH
 
 
def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False
 
def plat_gen():
    while len(platforms) < 6:
        width = random.randrange(50,100)
        p  = Platform()      
        C = True
         
        while C:
             p = Platform()
             p.rect.center = (random.randrange(0, WIDTH - width),
                              random.randrange(-70, 0))
             C = check(p, platforms)
        platforms.add(p)
        all_sprites.add(p)
 
class Wind(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()      
        self.speed = random.randint(-1, 1)
        self.moving = bool(random.getrandbits(1))
        self.time = self.gen_rand_time()
        self.active = False
        self.strength = 0.00

    def gen_rand_time(self):
        max_seconds = 2
        return random.randint(0,FPS*max_seconds)
    
    def gen_rand_strength(self):
        max_strength = 100
        return (random.random() - 0.5) * 2 * max_strength
 
    def update(self):
        self.time -= 1
        if self.time <= 0:
            self.time = self.gen_rand_time()
            self.active = not self.active
            self.strength = self.gen_rand_strength()

    def get_wind_val(self):
        if self.active:
            return self.strength
        else:
            return 0
        
            
        
 
        
PT1 = Platform()
P1 = Player()
 
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
PT1.moving = False

wind = Wind()
 
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)
#all_sprites.add(wind)
 
platforms = pygame.sprite.Group()
platforms.add(PT1)
 
for x in range(random.randint(4,5)):
    C = True
    pl = Platform()
    while C:
        pl = Platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)
 
arduino_position = 0
while True:
    # read data from Arduino
    # arduino_data = str(arduino.readline())[:-5]
    # arduino_position = float(arduino_data.split(":")[1]) # "rel_position:-17.00"
    
    arduino_data = str(arduino.readline())
    
    arduino_position_str = arduino_data.split("\\r")
    arduino_position_str = arduino_position_str[0]
    try:
        arduino_position = float(arduino_position_str[2:])
    except ValueError as e:
        print("had a little oopsie", arduino_position_str)
        arduino_position = arduino_position
    if arduino_position < -45:
        arduino_position = -45
    if arduino_position > 45:
        arduino_position = 45
    P1.pos.x = ((arduino_position + 45) / 90) * WIDTH 

    # write data to Arduino
    wind_force = int(wind.get_wind_val())
    arduino.write(bytes(str(wind_force).encode()))

    wind.update()
    print(wind_force)

    # Update the game state
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()  
 
    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()

    if P1.rect.top > HEIGHT: #P1 goes underneath the bottom of the screen
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            displaysurface.fill((255,0,0))
            pygame.display.update()
            time.sleep(1)
            pygame.quit()
            exit()
 
    plat_gen()
    displaysurface.fill((0,0,0))
     
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()
 
    pygame.display.update()
    FramePerSec.tick(FPS)