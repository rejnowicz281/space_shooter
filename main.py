import random

import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((700, 700))

# Background
background = pygame.image.load('background.jpg')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Score

score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
score_x = 10
score_y = 10


def show_score(x, y):
    score = score_font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 100)


def show_game_over():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (50, 310))


# Title and Icon
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load('spaceship.png')
playerX = 310
playerY = 500
playerX_change = 0

# Enemies
enemies = []
for i in range(5):
    enemy = {
        "img": pygame.image.load('ghost(1).png'),
        "x": random.randint(100, 600),
        "y": random.randint(64, 128),
        "x_change": 1,
        "y_change": 100
    }
    enemies.append(enemy)

# Bullet
bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 0
bulletY_change = 0
bullet_state = "ready"


def draw_player(x, y):
    screen.blit(player_img, (x, y))


def draw_enemy(enemy_img, x, y):
    screen.blit(enemy_img, (x, y))


def draw_bullet(x, y):
    screen.blit(bullet_img, (x, y))


def is_collision(bullet_x, bullet_y, enemy_x, enemy_y):
    return (enemy_y - 48) < bullet_y < (enemy_y + 48) and (enemy_x - 16) < bullet_x < (enemy_x + 48)


# Game Loop
running = True
while running:

    screen.fill((82, 100, 150))
    # Background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if pressing arrows, move left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            elif event.key == pygame.K_RIGHT:
                playerX_change = 1
            elif event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletY_change = -2
                bulletX = playerX + 16
                bulletY = playerY - 32
                bullet_state = "fired"
                mixer.Sound('laser.wav').play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for player boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 636:
        playerX = 636

    for enemy in enemies:
        # Spawn enemies
        draw_enemy(enemy["img"], enemy["x"], enemy["y"])

        # Enemy movement
        enemy["x"] += enemy["x_change"]
        if enemy["x"] <= 0 or enemy["x"] >= 636:
            enemy["x_change"] *= -1
            enemy["y"] += enemy["y_change"]

        # Game Over
        if enemy["y"] > 500:
            # Make sure all enemies disappear
            for enemy_b in enemies:
                enemy_b["y"] = 2000
            show_game_over()

    # Bullet behaviour if fired
    if bullet_state == "fired":
        draw_bullet(bulletX, bulletY)
        bulletY += bulletY_change
        for enemy in enemies:
            if is_collision(bulletX, bulletY, enemy["x"], enemy["y"]):
                mixer.Sound('explosion.wav').play()
                bullet_state = "ready"
                score_value += 1
                enemy["x"] = random.randint(100, 600)
                enemy["y"] = random.randint(64, 128)
                print(score_value)
    if bulletY <= -32:
        bullet_state = "ready"

    # Spawn player
    draw_player(playerX, playerY)

    show_score(score_x, score_y)
    pygame.display.update()
