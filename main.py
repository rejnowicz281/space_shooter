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
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))


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
                playerX_change = -0.3
            elif event.key == pygame.K_RIGHT:
                playerX_change = 0.3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    player(playerX, playerY)
    pygame.display.update()
