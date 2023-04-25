import pygame
import random

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((700, 700))

# Title and Icon
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load('spaceship.png')
playerX = 310
playerY = 500
playerX_change = 0

# Enemy
enemy_img = pygame.image.load('ghost(1).png')
enemyX = random.randint(100, 600)
enemyY = random.randint(64, 128)
enemyX_change = 0.3
enemyY_change = 40

def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y):
    screen.blit(enemy_img, (x, y))


# Game Loop
running = True
while running:

    screen.fill((82, 100, 150))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if pressing arrows, move left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 0.5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for player boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 636:
        playerX = 636

    # Enemy movement
    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change += 0.3
        enemyY += enemyY_change
    elif enemyX >= 636:
        enemyX_change -= 0.3
        enemyY += enemyY_change

    player(playerX, playerY)
    enemy(enemyX, enemyY)

    pygame.display.update()
