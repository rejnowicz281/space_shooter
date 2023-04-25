import pygame

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((700, 700))

# Title and Icon
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 310
playerY = 500


def player():
    screen.blit(playerImg, (playerX, playerY))


# Game Loop
running = True
while running:

    screen.fill((82, 100, 150))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player()
    pygame.display.update()