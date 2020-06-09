import pygame
import random
import math
from pygame import mixer

# inititalizing pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Title, icon and background

pygame.display.set_caption("Sushan's Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Background

background = pygame.image.load('background.jpg')

# Background Sound

mixer.music.load('background.wav')
mixer.music.play(-1)


# Player
playerimg = pygame.image.load('player.png')
playerx = 370
playery = 480
playerx_change = 0

#Enemy list
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
numofenemies = 10


# Enemy
for i in range(numofenemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(5)
    enemyy_change.append(40)

# Bullet
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 20
bullet_state = "ready"


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i] , (x, y))


def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx-bulletx, 2)) + (math.pow(enemyy-bullety, 2)))

    if distance <= 27:
        return True
    else:
        return False

#Score 'freesansbold.ttf'

score_value = 0
font = pygame.font.SysFont('calibri.ttf', 32)
textx = 10
texty = 10

def show_value(x, y):
    score = font.render("Score: "+ str(score_value) , True, (255, 255, 0))
    screen.blit(score, (x, y))

#Game Over

over_text = pygame.font.SysFont('calibri.ttf', 64)

def gameover():
    over = over_text.render("GAME OVER", True, (255, 255, 0))
    screen.blit(over, (255, 200))


# Game Loop
running = True
while running:
    # Red, Green, Blue
    screen.fill((0, 255, 255))

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerx_change = -20
            if event.key == pygame.K_RIGHT:
                playerx_change = 20
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletsound = mixer.Sound('laser.wav')
                    bulletsound.play()
                    bulletx = playerx
                    bullet_fire(bulletx, bullety)

        if event.type == pygame.KEYUP:
            playerx_change = 0

    # Player's movement
    playerx += playerx_change

    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

        # Enemy's movement
    for i in range(numofenemies):
        if enemyy[i] > 400:
            for j in range(numofenemies):
                enemyy[j] =2000
                gameover()
            break
        enemyx[i] += enemyx_change[i]

        if enemyx[i] <= 0:
            enemyx_change[i] = 5
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -5
            enemyy[i] += enemyy_change[i]

        # collision
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            collision = mixer.Sound('explosion.wav')
            collision.play()
            bullety = 480
            bullet_state = "ready"
            score_value += 1

            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)

        enemy(enemyx[i], enemyy[i], i)

    # Bullet movement

    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        bullet_fire(bulletx, bullety)
        bullety -= bullety_change





    player(playerx, playery)
    show_value(textx, texty)
    pygame.display.update()
