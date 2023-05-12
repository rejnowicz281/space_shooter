import random
from spritesheet import Spritesheet
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Create screen
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Background
background = pygame.image.load('graphics/background.png').convert()

# Background Music
mixer.music.load('audio/background.wav')
mixer.music.play(-1)

main_font = pygame.font.Font('font/dogicapixelbold.ttf', 32)


def draw_text(x, y, text, font=main_font, color=(255, 255, 255)):
    content = font.render(text, True, color)
    content_rect = content.get_rect(center=(x, y))
    screen.blit(content, content_rect)


# Title and Icon
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load('graphics/icon.png')
pygame.display.set_icon(icon)


class Player(pygame.sprite.Sprite):
    def __init__(self, x=SCREEN_WIDTH / 2, y=650):
        super().__init__()
        self.anim_index = 0
        self.sprites = self.get_ship_sprites()
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        self.bullets = pygame.sprite.Group(Bullet(), Bullet(), Bullet("flame"))
        self.bullets_follow_ship()

    @staticmethod
    def get_ship_sprites():
        sheet = Spritesheet("graphics/player/ship.png")
        return [sheet.get_sprite(0, 0, 16, 24, 4), sheet.get_sprite(0, 1, 16, 24, 4), sheet.get_sprite(0, 2, 16, 24, 4),
                sheet.get_sprite(0, 3, 16, 24, 4), sheet.get_sprite(0, 4, 16, 24, 4),
                sheet.get_sprite(1, 0, 16, 24, 4), sheet.get_sprite(1, 1, 16, 24, 4), sheet.get_sprite(1, 2, 16, 24, 4),
                sheet.get_sprite(1, 3, 16, 24, 4), sheet.get_sprite(1, 4, 16, 24, 4)]

    def bullets_follow_ship(self):
        bullet1 = self.bullets.sprites()[0]
        bullet2 = self.bullets.sprites()[1]
        bullet3 = self.bullets.sprites()[2]

        if not bullet1.fired: bullet1.rect.center = (self.rect.centerx - 45, self.rect.centery)
        if not bullet2.fired: bullet2.rect.center = (self.rect.centerx + 35, self.rect.centery)
        if not bullet3.fired: bullet3.rect.center = (self.rect.centerx - 5, self.rect.centery - 50)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move_right()

    def fire(self):
        bullet1 = self.bullets.sprites()[0]  # Ball 1
        bullet2 = self.bullets.sprites()[1]  # Ball 2
        bullet3 = self.bullets.sprites()[2]  # Flame 1

        if not bullet3.fired:
            bullet3.fire()
        elif not bullet1.fired:
            bullet1.rect.centerx = self.rect.centerx - 5
            bullet1.fire()
        elif not bullet2.fired:
            bullet2.rect.centerx = self.rect.centerx - 5
            bullet2.fire()

    def move_left(self):
        self.rect.x -= self.speed
        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def animate(self):
        self.anim_index += 0.2
        if self.anim_index >= len(self.sprites): self.anim_index = 0
        self.image = self.sprites[int(self.anim_index)]

    def update(self):
        self.input()
        self.animate()
        self.bullets_follow_ship()
        self.bullets.update()
        self.bullets.draw(screen)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_type="ball", x=0, y=0):
        super().__init__()
        self.bullet_type = bullet_type
        self.sprites = self.get_sprites()
        self.anim_index = 0
        self.image = self.sprites[self.anim_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        self.fired = False

    def get_sprites(self):
        sheet = Spritesheet("graphics/bullet.png")
        if self.bullet_type == "ball":
            return [sheet.get_sprite(0, 0, 14, 16, 3), sheet.get_sprite(0, 1, 14, 16, 3)]
        elif self.bullet_type == "flame":
            return [sheet.get_sprite(1, 0, 14, 16, 3), sheet.get_sprite(1, 1, 14, 16, 3)]

    def animate(self):
        self.anim_index += 0.1
        if self.anim_index >= len(self.sprites): self.anim_index = 0
        self.image = self.sprites[int(self.anim_index)]

    def update(self):
        if self.fired and self.rect.bottom > 0:  # If bullet is fired and is not off-screen
            self.move()
            self.animate()
        else:
            self.fired = False

    def move(self):
        self.rect.y -= self.speed

    def fire(self):
        self.fired = True
        laser_sound = mixer.Sound('audio/laser.wav')
        laser_sound.play()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type="medium", x=0, y=0):
        super().__init__()
        self.enemy_type = enemy_type
        self.sprites = self.get_sprites()
        self.anim_index = 0
        self.image = self.sprites[self.anim_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.randomize_position()
        self.speed = 3

    def get_sprites(self):
        if self.enemy_type == "small":
            sheet = Spritesheet("graphics/enemy/enemy-small.png")
            return [sheet.get_sprite(0, 0, 16, 16, 4), sheet.get_sprite(0, 1, 16, 16, 4)]
        elif self.enemy_type == "medium":
            sheet = Spritesheet("graphics/enemy/enemy-medium.png")
            return [sheet.get_sprite(0, 0, 32, 16, 3), sheet.get_sprite(0, 1, 32, 16, 3)]
        elif self.enemy_type == "big":
            sheet = Spritesheet("graphics/enemy/enemy-big.png")
            return [sheet.get_sprite(0, 0, 32, 32, 3), sheet.get_sprite(0, 1, 32, 32, 3)]

    def update(self):
        self.move()
        self.animate()

    def animate(self):
        self.anim_index += 0.1
        if self.anim_index >= len(self.sprites): self.anim_index = 0
        self.image = self.sprites[int(self.anim_index)]

    def reset(self):
        self.sprites = self.get_sprites()
        self.randomize_position()

    def move(self):
        self.rect.x += self.speed
        if self.rect.x < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed *= -1
            self.rect.y += 100

    def explode(self):
        self.reset()
        explosion_sound = mixer.Sound('audio/explosion.wav')
        explosion_sound.set_volume(0.3)
        explosion_sound.play()

    def randomize_position(self):
        self.rect.centerx = random.randint(self.image.get_width() * 2, SCREEN_WIDTH - (self.image.get_width() * 2))
        self.rect.centery = random.randint(self.image.get_height(), self.image.get_height() * 2)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.sprites = self.get_sprites()
        self.anim_index = 0
        self.image = self.sprites[self.anim_index]
        self.rect = self.image.get_rect(center=(x, y))

    @staticmethod
    def get_sprites():
        sheet = Spritesheet("graphics/explosion.png")
        return [sheet.get_sprite(0, 0, 16, 16, 4), sheet.get_sprite(0, 1, 16, 16, 4), sheet.get_sprite(0, 2, 16, 16, 4),
                sheet.get_sprite(0, 3, 16, 16, 4), sheet.get_sprite(0, 4, 16, 16, 4)]

    def update(self):
        self.anim_index += 0.2
        if self.anim_index >= len(self.sprites):
            self.kill()
        else:
            self.image = self.sprites[int(self.anim_index)]


class Game:
    def __init__(self):
        self.state = "running"
        self.explosions = pygame.sprite.Group()
        self.high_score = self.load_high_score()
        self.score = 0
        self.player = pygame.sprite.GroupSingle(Player())
        self.enemies = pygame.sprite.Group()
        [self.add_enemy() for i in range(5)]

    def update(self):
        self.player.update()
        self.player.draw(screen)

        self.show_score()
        self.show_high_score()

        if self.state == "running":
            self.enemies.draw(screen)
            self.enemies.update()
            self.collision_check()

            self.explosions.update()
            self.explosions.draw(screen)
        elif self.state == "game_over":
            mixer.music.stop()
            self.show_game_over()

    def collision_check(self):
        for bullet in self.player.sprite.bullets:
            bullet_hit_list = pygame.sprite.spritecollide(bullet, self.enemies, False)
            for enemy in bullet_hit_list:
                self.explosions.add(pygame.sprite.GroupSingle(Explosion(enemy.rect.centerx, enemy.rect.centery)))
                enemy.explode()
                bullet.fired = False
                self.increase_score()

        for enemy in self.enemies:
            if enemy.rect.y > 600:
                self.destroy_enemies()
                self.state = "game_over"

    def add_enemy(self):
        self.enemies.add(Enemy())

    def destroy_enemies(self):
        self.enemies.empty()

    def increase_score(self):
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score

    @staticmethod
    def load_high_score():
        try:
            with open("high_score.txt", "r") as high_score_file:
                return int(high_score_file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open("high_score.txt", "w") as high_score_file:
            high_score_file.write(str(self.high_score))

    def show_score(self):
        draw_text(SCREEN_WIDTH / 2, 70, "SCORE: " + str(self.score))

    def show_high_score(self):
        draw_text(SCREEN_WIDTH / 2, 30, "HIGH SCORE: " + str(self.high_score))

    def show_game_over(self):
        font = pygame.font.Font('font/dogicapixelbold.ttf', 76)
        draw_text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, "GAME OVER", font)


# Game Loop
game = Game()
running = True
while running:
    # Ensure 60 FPS
    pygame.time.Clock().tick(60)

    # Background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.save_high_score()
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game.player.sprite.fire()

    game.update()

    pygame.display.update()
