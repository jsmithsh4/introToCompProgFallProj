# Sources:https://www.geeksforgeeks.org/python-program-to-calculate-acceleration-final-velocity-initial-velocity-and-time/
# https://coderslegacy.com/python/python-pygame-tutorial/
# https://www.youtube.com/watch?v=hDu8mcAlY4E
# https://stackoverflow.com/questions/59656876/making-a-platform-in-pygame

# Imports Libraries 
import pygame
from pygame.locals import *
import sys
import random
import time
 
# Code initializes pygame ands sets the 2D
pygame.init()
vec = pygame.math.Vector2 
 
#Sets up the display window alng with the friction and the acceleration. The Frames per second is also established 
HEIGHT = 400
WIDTH = 400
ACC = 0.62
FRIC = -0.11
FPS = 60

#Sets up FPS to be linked with the game 
FramePerSec = pygame.time.Clock()
 
#Sets the display window
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JUMP")
#Sets up player class along with attributes of player. Color, position, starting score etc.
class BLOCK(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,0,128))
        self.rect = self.surf.get_rect()
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
        self.score = 0 
    # Sets up the movie function that allows movement for the player. This also assigns keys that corresond for the movements
    def move (self):
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
    # Sets up the jump function for the player. The code below allows the block to jump and also implements the collide feature.
    def jump(self): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15
 
#  Update allows the constant tracking of the block so that the code can tell if the block is on top of a platform or not. Aslo has a score value that is implemented to the platforms 
    def update(self):
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:   
                        hits[0].point = False   
                        self.score += 1          
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
 
#Class sets up attributes for the platforms in the code. The creates random placements and movements for the platforms.
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10),
                                                 random.randint(0, HEIGHT-30)))
        self.speed = random.randint(-1, 1)
        
        self.point = True   
        self.moving = True
        
    
    def move(self):
        if self.moving == True:  
            self.rect.move_ip(self.speed,0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH
 
# This code checks if the platforms are too close to each other so that they are not overlapping
def Lcheck(platform, platstore):
    if pygame.sprite.spritecollideany(platform,platstore):
        return True
    else:
        for entity in platstore:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False
#  This code compliments the one above checking if the value is returning true or not
def plat_gen():
    while len(platforms) < 6:
        width = random.randrange(50,100)
        p  = platform()      
        C = True
         
        while C:
             p = platform()
             p.rect.center = (random.randrange(0, WIDTH - width),
                              random.randrange(-50, 0))
             C = Lcheck(p, platforms)
        platforms.add(p)
        all_sprites.add(p)
 
 
# Labels and names for created classes 
PT1 = platform()
P1 = BLOCK()
 
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((240,248,255))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
 
#Allows access to all sprites so that they are all called in the code 
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)
 
platforms = pygame.sprite.Group()
platforms.add(PT1)

PT1.moving = False
PT1.point = False   

for x in range(random.randint(4,5)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = Lcheck(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)
 
#  Implements a quit function 
while True:
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump()
    # code kills the block if it goes below the screen and has a deaht screen 
    if P1.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            displaysurface.fill((255,0,0))
            pygame.display.update()
            time.sleep(1)
            pygame.quit()
            sys.exit()
 
    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
 
    plat_gen()
    displaysurface.fill((0,0,0))
    f = pygame.font.SysFont("Verdana", 20)     
    g  = f.render(str(P1.score), True, (123,255,0))   
    displaysurface.blit(g, (WIDTH/2, 10))   
     
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()
#  Updates the game as it goes
    pygame.display.update()
    FramePerSec.tick(FPS)
