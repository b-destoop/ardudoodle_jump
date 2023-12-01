import random
import serial
import pygame
from pygame.locals import *
import time

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

#arduino = serial.Serial(port="COM15", baudrate=115200, timeout=0.01)
#time.sleep(.01)

pygame.init()
vec = pygame.math.Vector2 # 2 for two dimentional

FramePerSec = pygame.time.Clock()
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 200))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

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

        # screen wrapping => infinitely move across the borders of the screen 
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        
        self.rect.midbottom = self.pos

    def update(self):
        hits = pygame.sprite.spritecollide(P1 , platforms, False)
        if hits:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0

    def jump(self):
        self.vel.y = -15
 
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10),
                                                 random.randint(0,HEIGHT-30)))
    def move(self):
        pass
        
def plat_gen():
    while len(platforms) < 7:
        width = random.randrange(50, 100)
        p = Platform()
        p.rect.center = (random.randrange(0, WIDTH - width),
                         random.randrange(-50, 0))
        platforms.add(p)
        all_sprites.add(p)
 
PT1 = Platform()
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((250, 0, 0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

# setup (run once)
for x in range(random.randint(5,6)):
    pl = Platform()
    platforms.add(pl)
    all_sprites.add(pl)

# game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()

    if P1.rect.top <= HEIGHT/3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()


    displaysurface.fill((0,0,0))
    
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()
        entity.update()

    plat_gen()

    
    pygame.display.update()
    FramePerSec.tick(FPS)
