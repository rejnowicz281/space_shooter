import pygame


class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

    def get_sprite(self, x, y, width, height, scale=1):
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        sprite = pygame.transform.rotozoom(sprite, 0, scale)
        sprite.set_colorkey((0, 0, 0))

        return sprite
