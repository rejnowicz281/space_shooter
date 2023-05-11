import pygame


class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

    def get_sprite(self, row, column, width, height, scale=3):
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sprite_sheet, (0, 0), (column * width, row * height, width, height))
        sprite = pygame.transform.scale_by(sprite, scale)
        sprite.set_colorkey((0, 0, 0))

        return sprite
