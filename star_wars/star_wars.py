from operator import truediv
from pickletools import pystring
from time import time
from turtle import speed
import pygame
import random

def starwar(screen):
    FPS = 60
    game=True
    UfoArray = pygame.sprite.Group()
    timer = 0
    bullets = pygame.sprite.Group()
    asteroidGroup = pygame.sprite.Group()
    hp = 5
    points = 0
    healArray = pygame.sprite.Group()
    pygame.font.init()

    font = pygame.font.Font('star_wars/a_FuturaRound Bold.ttf', 65)
    hpLabel = font.render('HP ' + str(hp),True,(255,255,255))
    pointLabel = font.render('KILLS ' + str(points),True,(255,255,255))

    class Sprite(pygame.sprite.Sprite):
        def __init__(self,x,y, w, h, imagefile,speed = 5):
            pygame.sprite.Sprite.__init__(self)
            self.rect = pygame.Rect(x,y,w,h)
            self.image = pygame.image.load(imagefile)
            self.image = pygame.transform.scale(self.image, (w,h))
            self.speed = speed
        def ShowSprite(self):
            win.blit(self.image, (self.rect.x, self.rect.y))
        def update(self):
            keys = pygame.key.get_pressed() 
            if(keys[pygame.K_LEFT]):
                self.rect.x -=5
            if(keys[pygame.K_RIGHT]):
                self.rect.x +=5
                
    class Ufo(Sprite):
        def update(self):
            self.rect.y += self.speed
            
    class Bullet(Sprite):
        def update(self):
            self.rect.y -= self.speed
    class Asteroid(Sprite):
        def update(self):
            self.rect.y += self.speed
    class Heal(Sprite):
        def update(self):
            self.rect.y += self.speed

    win=pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    HealthItem = Heal(320,440 , 30,40, 'star_wars/HealItem.png')

    player = Sprite(320,440 , 60,60, 'star_wars/rocket.png')
    for i in range(5):
        enemy = Ufo(random.randint(0,11) * 60, random.randint(-300,-150), 65,40, 'star_wars/ufo.png', random.randint(1,5))
        UfoArray.add(enemy)

    backgound = pygame.image.load('star_wars/star_war_bg.jpeg')
    backgound = pygame.transform.scale(backgound, (800, 600))
    GameOverSprite = pygame.image.load('star_wars/game-over-screen.jpg')
    GameOverSprite = pygame.transform.scale(GameOverSprite, (800, 600))

    pygame.display.update()

    while game:
        win.blit(backgound, (0,0))

        clock.tick(FPS)
        timer += 1
        if(timer % 60 == 0):
            enemy = Ufo(random.randint(0,11) * 60, random.randint(-300,-150), 65,40, 'star_wars/ufo.png', random.randint(1,5))
            UfoArray.add(enemy)
        if(timer % 180 == 0):
            asteroid = Asteroid(random.randint(0,11) * 60, random.randint(-300,-150), 65,40, 'star_wars/asteroid.png', random.randint(1,5))
            asteroidGroup.add(asteroid)
        if(timer % 200 == 0):
            healSpawn = Heal(random.randint(0,11) * 60, random.randint(-300,-150), 65,40, 'star_wars/HealItem.png', random.randint(1,2))
            healArray.add(healSpawn)
            
        if(pygame.sprite.groupcollide(UfoArray,bullets, True, True)):
            points += 1
            pointLabel = font.render('KILLS ' + str(points),True,(255,255,255))
        pygame.sprite.groupcollide(asteroidGroup,bullets, False, True)
        
        # while 2
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                game=False
            if(i.type == pygame.KEYDOWN):
                if(i.key == pygame.K_SPACE):
                    bullets.add(Bullet(player.rect.centerx - 12, player.rect.top, 20,20, 'star_wars/bullet.png', 4))
                
        for e in healArray:
            if(player.rect.colliderect(e.rect)):
                print('+hp')
                hp += 1
                hpLabel = font.render('HP' + str(hp),True,(255,255,255))
                healArray.remove(e)
                
        for e in asteroidGroup:
            if(player.rect.colliderect(e.rect)):
                print('ohhh')
                hp -= 2
                hpLabel = font.render('HP' + str(hp),True,(255,255,255))
                asteroidGroup.remove(e)
        for e in UfoArray:
            if(player.rect.colliderect(e.rect)):
                print('ohhh noo')
                hp -= 1
                hpLabel = font.render('HP' + str(hp),True,(255,255,255))
                UfoArray.remove(e)
        if(hp <= 0):
            game = False
                
        player.update()
        UfoArray.update()
        bullets.update()
        asteroidGroup.update()
        healArray.update()
        player.ShowSprite()
        win.blit(hpLabel, (40,20))
        win.blit(pointLabel, (40,80))
        
        for k in UfoArray:
            k.ShowSprite()
        for b in bullets:
            b.ShowSprite()
        for a in asteroidGroup:
            a.ShowSprite()
        for a in healArray:
            a.ShowSprite()

        pygame.display.update()
    game = True
    PointControll = font.render('YOU SCORE IS  ' + str(points),True,(150,0,0))

    while game:
        win.fill((125,125,125))
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                game=False
        win.blit(PointControll, (50,150))
        pygame.display.update()

starwar(screen=1)