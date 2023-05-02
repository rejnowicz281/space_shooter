import os
import random

import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Create screen
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Background
background = pygame.image.load('background.jpg')

# Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)


def draw_text(x, y, text, font=pygame.font.Font('freesansbold.ttf', 32), color=(255, 255, 255)):
    content = font.render(text, True, color)
    screen.blit(content, (x, y))


# Title and Icon
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)


class Player:
    PLAYER_LINE = SCREEN_HEIGHT - 200

    def __init__(self):
        self.img = pygame.image.load('spaceship.png')
        self.x = SCREEN_WIDTH / 2 - self.img.get_width() / 2
        self.y = self.PLAYER_LINE
        self.speed = 10
        self.bullet = Bullet()

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH - self.img.get_width():
            self.x = SCREEN_WIDTH - self.img.get_width()

    def shoot_bullet(self):
        self.bullet.x = self.x + self.img.get_width() / 4
        self.bullet.y = self.y - self.img.get_height() / 2
        self.bullet.fired = True
        mixer.Sound('laser.wav').play()


class Bullet:
    def __init__(self):
        self.img = pygame.image.load('bullet.png')
        self.x = 0
        self.y = 0
        self.speed = 10
        self.fired = False

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.y -= self.speed

    def update(self):
        if self.fired and self.y > -self.img.get_height():  # If bullet is fired and is not off-screen
            self.move()
            self.draw()
        else:
            self.fired = False


class Enemy:
    FADE_IN_SPEED = 15

    def __init__(self):
        self.img = None
        self.randomize_image()
        self.x = 0
        self.y = 0
        self.randomize_position()
        self.speed = 8
        self.alpha = 0

    def draw(self):
        if self.alpha < 255:
            self.img.set_alpha(self.alpha)
            self.alpha += self.FADE_IN_SPEED

        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.speed
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.img.get_width():
            self.speed *= -1
            self.y += 100

    def randomize_position(self):
        self.x = random.randint(self.img.get_width() * 2, SCREEN_WIDTH - (self.img.get_width() * 2))
        self.y = random.randint(self.img.get_height(), self.img.get_height() * 2)

    def randomize_image(self):
        enemy_images = os.listdir("Enemies")
        self.img = pygame.image.load(f"Enemies/{random.choice(enemy_images)}")

    def reset(self):
        self.randomize_image()
        self.randomize_position()
        self.alpha = 0

    def explode(self):
        self.reset()
        mixer.Sound('explosion.wav').play()


class Game:
    def __init__(self):
        self.state = "running"
        self.high_score = 0
        self.load_high_score()
        self.score = 0
        self.player = Player()
        self.enemies = []
        [self.add_enemy() for _ in range(5)]

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.move()
            enemy.draw()

            if self.player.bullet.fired and \
                    (enemy.y - 48) < self.player.bullet.y < (enemy.y + 48) and \
                    (enemy.x - 16) < self.player.bullet.x < (enemy.x + 48):  # Bullet - enemy collision detection
                enemy.explode()
                self.player.bullet.fired = False
                self.increase_score()

            if enemy.y > Player.PLAYER_LINE:
                self.destroy_enemies()
                self.state = "game_over"

    def add_enemy(self):
        self.enemies.append(Enemy())

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as high_score_file:
                self.high_score = int(high_score_file.read())
        except FileNotFoundError:
            self.high_score = 0

    def save_high_score(self):
        with open("high_score.txt", "w") as high_score_file:
            high_score_file.write(str(self.high_score))

    def show_score(self):
        draw_text(10, 50, "Score: " + str(self.score))

    def show_high_score(self):
        draw_text(10, 10, "High Score: " + str(self.high_score))

    def show_game_over(self):
        font = pygame.font.Font('freesansbold.ttf', 100)
        draw_text(50, 310, "GAME OVER", font)

    def increase_score(self):
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score

    def destroy_enemies(self):
        self.enemies = []


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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game.player.bullet.fired:
                game.player.shoot_bullet()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        game.player.move_left()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        game.player.move_right()

    if game.state == "running":
        game.update_enemies()
    elif game.state == "game_over":
        game.show_game_over()

    game.player.draw()
    game.player.bullet.update()

    game.show_score()
    game.show_high_score()
    pygame.display.update()
