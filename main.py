import pygame

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((600, 600))

# Title and Icon
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False