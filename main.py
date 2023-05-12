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
icon = pygame.image.load('graphics/spaceship/ship_blue.png')
pygame.display.set_icon(icon)


def get_ship_image(color):
    if "blue" != color != "red": color = random.choice(["red", "blue"])
    image = pygame.image.load(f"graphics/spaceship/ship_{color}.png").convert_alpha()
    image = pygame.transform.rotozoom(image, 0, 1.5)

    return image


def get_alien_sprites():
    alien_id = random.randint(1, 3)
    alien_color = random.choice(["g", "p", "r", "y"])

    sprites = {}
    main = Spritesheet(f'graphics/alien/alien{alien_id}_{alien_color}.png')
    if alien_id == 1:
        sprites["main"] = [main.get_sprite(0, 0, 32, 32, 2), main.get_sprite(0, 1, 32, 32, 2),
                           main.get_sprite(0, 2, 32, 32, 2),
                           main.get_sprite(1, 0, 32, 32, 2), main.get_sprite(1, 1, 32, 32, 2),
                           main.get_sprite(1, 2, 32, 32, 2),
                           main.get_sprite(2, 0, 32, 32, 2), main.get_sprite(2, 1, 32, 32, 2)]
    elif alien_id == 2:
        sprites["main"] = [main.get_sprite(0, 0, 32, 32, 2), main.get_sprite(0, 1, 32, 32, 2),
                           main.get_sprite(0, 2, 32, 32, 2),
                           main.get_sprite(1, 0, 32, 32, 2), main.get_sprite(1, 1, 32, 32, 2),
                           main.get_sprite(1, 2, 32, 32, 2),
                           main.get_sprite(2, 0, 32, 32, 2)]
    elif alien_id == 3:
        sprites["main"] = [main.get_sprite(0, 0, 32, 32, 2), main.get_sprite(0, 1, 32, 32, 2),
                           main.get_sprite(1, 0, 32, 32, 2), main.get_sprite(1, 1, 32, 32, 2)]

    return sprites


class Player(pygame.sprite.Sprite):
    def __init__(self, x=SCREEN_WIDTH / 2, y=650, ship_color=random.choice(["red", "blue"])):
        super().__init__()
        self.image = get_ship_image(ship_color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        self.bullet = pygame.sprite.GroupSingle(Bullet())

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move_right()
        if keys[pygame.K_SPACE] and not self.bullet.sprite.fired:
            self.bullet.sprite.fire()

    def move_left(self):
        self.rect.x -= self.speed
        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def update(self):
        self.bullet.update()
        if not self.bullet.sprite.fired:  # Bullet stays beside ship if it is not fired
            self.bullet.sprite.rect.center = (self.rect.right - 5, self.rect.centery)
        self.bullet.draw(screen)
        self.input()


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = 10
        self.fired = False

    def update(self):
        if self.fired and self.rect.bottom > 0:  # If bullet is fired and is not off-screen
            self.move()
        else:
            self.fired = False

    def move(self):
        self.rect.y -= self.speed

    def fire(self):
        self.fired = True
        mixer.Sound('audio/laser.wav').play()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.anim_index = 0
        self.sprites = get_alien_sprites()
        self.image = self.sprites["main"][0]
        self.rect = self.image.get_rect()
        self.randomize_position()
        self.speed = 3
        self.alpha = 0

    def update(self):
        self.move()
        self.animate()

    def animate(self):
        for _ in range(len(self.sprites["main"])):
            self.anim_index += 0.05
            if self.anim_index >= len(self.sprites["main"]): self.anim_index = 0
            self.image = self.sprites["main"][int(self.anim_index)]

    def reset(self):
        self.sprites = get_alien_sprites()
        self.randomize_position()
        self.alpha = 0

    def move(self):
        self.rect.x += self.speed
        if self.rect.x < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed *= -1
            self.rect.y += 100

    def explode(self):
        self.reset()
        mixer.Sound('audio/explosion.wav').play()

    def randomize_position(self):
        self.rect.centerx = random.randint(self.image.get_width() * 2, SCREEN_WIDTH - (self.image.get_width() * 2))
        self.rect.centery = random.randint(self.image.get_height(), self.image.get_height() * 2)


class Game:
    def __init__(self):
        self.state = "running"
        self.high_score = self.load_high_score()
        self.score = 0
        self.player = pygame.sprite.GroupSingle(Player())
        self.enemies = pygame.sprite.Group()
        [self.add_enemy() for i in range(5)]

    def update(self):
        self.player.draw(screen)
        self.player.update()

        self.show_score()
        self.show_high_score()

        if self.state == "running":
            self.enemies.draw(screen)
            self.enemies.update()
            self.collision_check()
        elif self.state == "game_over":
            mixer.music.stop()
            self.show_game_over()

    def collision_check(self):
        if self.player.sprite.bullet.sprite.fired:
            bullet_hit_list = pygame.sprite.spritecollide(self.player.sprite.bullet.sprite, self.enemies, False)
            for enemy in bullet_hit_list:
                enemy.explode()
                self.player.sprite.bullet.sprite.fired = False
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

    game.update()

    pygame.display.update()
