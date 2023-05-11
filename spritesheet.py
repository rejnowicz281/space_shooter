import pygame


class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

    def get_sprite(self, column, row, width, height, scale=1):
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sprite_sheet, (0, 0), (row * width, column * height, width, height))
        sprite = pygame.transform.rotozoom(sprite, 0, scale)
        sprite.set_colorkey((0, 0, 0))

        return sprite
