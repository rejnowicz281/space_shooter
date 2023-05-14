import math
import random
from spritesheet import Spritesheet
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
pygame.mouse.set_visible(False)

# Background
background = pygame.image.load('graphics/background.png').convert()

# Background Music
mixer.music.load('audio/background.wav')
mixer.music.play(-1)

main_font = pygame.font.Font('font/dogicapixelbold.ttf', 15)


def draw_text(x, y, text, font=main_font, color=(255, 255, 255)):
    content = font.render(text, True, color)
    content_rect = content.get_rect(center=(x, y))
    screen.blit(content, content_rect)


def draw_crosshair():
    pos = pygame.mouse.get_pos()
    cursor_img = pygame.image.load("graphics/crosshair.png").convert_alpha()
    cursor_img = pygame.transform.scale_by(cursor_img, 0.4)
    cursor_img_rect = cursor_img.get_rect(center=pos)
    screen.blit(cursor_img, cursor_img_rect)


# Title and Icon
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load('graphics/icon.png')
pygame.display.set_icon(icon)


class Player(pygame.sprite.Sprite):
    def __init__(self, x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2):
        super().__init__()
        self.anim_index = 0
        self.sprites = self.get_ship_sprites()
        self.image = self.get_current_image()
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0
        self.speed = 10
        self.bullets = pygame.sprite.Group()

    @staticmethod
    def get_ship_sprites():
        sheet = Spritesheet("graphics/player/ship.png")
        scale = 3
        return [sheet.get_sprite(0, 0, 16, 24, scale), sheet.get_sprite(0, 1, 16, 24, scale),
                sheet.get_sprite(0, 2, 16, 24, scale),
                sheet.get_sprite(0, 3, 16, 24, scale), sheet.get_sprite(0, 4, 16, 24, scale),
                sheet.get_sprite(1, 0, 16, 24, scale), sheet.get_sprite(1, 1, 16, 24, scale),
                sheet.get_sprite(1, 2, 16, 24, scale),
                sheet.get_sprite(1, 3, 16, 24, scale), sheet.get_sprite(1, 4, 16, 24, scale)]

    def reset(self):
        self.rect.x = SCREEN_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT / 2
        self.bullets = pygame.sprite.Group()

    def update(self):
        self.animate()
        self.point_towards_mouse()
        self.input()
        self.bullets.update()
        self.bullets.draw(screen)

    def animate(self):
        self.anim_index += 0.2
        if self.anim_index >= len(self.sprites): self.anim_index = 0
        self.image = self.get_current_image()

    def get_current_image(self):
        return self.sprites[int(self.anim_index)]

    def point_towards_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        self.angle = math.degrees(math.atan2(rel_x, rel_y)) - 180
        original_image = self.get_current_image()
        self.image = pygame.transform.rotate(original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def fire(self):
        bullet_type = "ball"
        self.bullets.add(Bullet(bullet_type, 15, 4, self.rect.centerx - 5, self.rect.centery, self.angle))

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move_right()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.move_up()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.move_down()

    def move_left(self):
        self.rect.x -= self.speed
        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def move_up(self):
        self.rect.y -= self.speed
        if self.rect.top < 0:
            self.rect.top = 0

    def move_down(self):
        self.rect.y += self.speed
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_type="ball", speed=15, scale=3, x=0, y=0, angle=0):
        super().__init__()
        self.scale = scale
        self.bullet_type = bullet_type
        self.anim_index = 0
        self.sprites = self.get_sprites()
        self.image = self.get_current_image()
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = speed
        mixer.Sound('audio/laser.wav').play()

    def get_sprites(self):
        sheet = Spritesheet("graphics/bullet.png")
        if self.bullet_type == "ball":
            return [sheet.get_sprite(0, 0, 14, 16, self.scale), sheet.get_sprite(0, 1, 14, 16, self.scale)]
        elif self.bullet_type == "flame":
            return [sheet.get_sprite(1, 0, 14, 16, self.scale), sheet.get_sprite(1, 1, 14, 16, self.scale)]

    def update(self):
        if 0 < self.rect.y < SCREEN_HEIGHT and 0 < self.rect.x < SCREEN_WIDTH:  # If bullet is on screen
            self.animate()
            self.rotate_with_angle()
            self.move()
        else:
            self.kill()

    def animate(self):
        self.anim_index += 0.1
        if self.anim_index >= len(self.sprites): self.anim_index = 0
        self.image = self.get_current_image()

    def get_current_image(self):
        return self.sprites[int(self.anim_index)]

    def rotate_with_angle(self):
        self.image = pygame.transform.rotate(self.image, self.angle)

    def move(self):
        x_vel = math.cos(-(self.angle - 270) * (2 * math.pi / 360)) * self.speed
        y_vel = math.sin(-(self.angle - 270) * (2 * math.pi / 360)) * self.speed

        self.rect.x += x_vel
        self.rect.y += y_vel

        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type="medium", x=0, y=0):
        super().__init__()
        self.enemy_type = enemy_type
        self.anim_index = 0
        self.sprites = self.get_sprites()
        self.image = self.get_current_image()
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0
        self.speed = 4
        self.shoot_delay = self.get_shoot_delay()
        self.bullets = pygame.sprite.Group()

    def get_sprites(self):
        if self.enemy_type == "small":
            sheet = Spritesheet("graphics/enemy/enemy-small.png")
            scale = 3
            return [sheet.get_sprite(0, 0, 16, 16, scale), sheet.get_sprite(0, 1, 16, 16, scale)]
        elif self.enemy_type == "medium":
            sheet = Spritesheet("graphics/enemy/enemy-medium.png")
            scale = 2
            return [sheet.get_sprite(0, 0, 32, 16, scale), sheet.get_sprite(0, 1, 32, 16, scale)]
        elif self.enemy_type == "big":
            sheet = Spritesheet("graphics/enemy/enemy-big.png")
            scale = 2
            return [sheet.get_sprite(0, 0, 32, 32, scale), sheet.get_sprite(0, 1, 32, 32, scale)]

    def update(self):
        self.move()
        self.fire()
        self.animate()
        self.bullets.update()
        self.bullets.draw(screen)

    def animate(self):
        self.anim_index += 0.1
        if self.anim_index >= len(self.sprites): self.anim_index = 0
        self.image = self.get_current_image()

    def get_current_image(self):
        return self.sprites[int(self.anim_index)]

    def fire(self):
        bullet_type = "flame"
        if self.shoot_delay <= 0:
            self.bullets.add(Bullet(bullet_type, 10, 3, self.rect.centerx - 5, self.rect.centery, self.angle - 180))
            self.shoot_delay = self.get_shoot_delay()
        else:
            self.shoot_delay -= 0.1

    @staticmethod
    def get_shoot_delay():
        return random.randint(5, 10)

    def move(self):
        x_vel = math.cos(-(self.angle - 90) * (2 * math.pi / 360)) * self.speed
        y_vel = math.sin(-(self.angle - 90) * (2 * math.pi / 360)) * self.speed

        self.rect.x += x_vel
        self.rect.y += y_vel

        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, scale=4):
        super().__init__()
        self.scale = scale
        self.sprites = self.get_sprites()
        self.anim_index = 0
        self.image = self.sprites[self.anim_index]
        self.rect = self.image.get_rect(center=(x, y))

    def get_sprites(self):
        sheet = Spritesheet("graphics/explosion.png")
        return [sheet.get_sprite(0, 0, 16, 16, self.scale), sheet.get_sprite(0, 1, 16, 16, self.scale),
                sheet.get_sprite(0, 2, 16, 16, self.scale),
                sheet.get_sprite(0, 3, 16, 16, self.scale), sheet.get_sprite(0, 4, 16, 16, self.scale)]

    def update(self):
        self.anim_index += 0.2
        if self.anim_index >= len(self.sprites):
            self.kill()
        else:
            self.image = self.sprites[int(self.anim_index)]


class Game:
    def __init__(self):
        self.paused = True
        self.explosions = pygame.sprite.Group()
        self.high_score = self.load_high_score()
        self.score = 0
        self.difficulty = 10
        self.player = pygame.sprite.GroupSingle(Player())
        self.enemies = pygame.sprite.Group()

    def update(self):
        self.explosions.update()
        self.explosions.draw(screen)

        if self.paused:
            mixer.music.stop()
            self.show_menu_screen()
        else:
            self.player.update()
            self.player.draw(screen)

            self.show_score()
            self.show_high_score()
            self.show_difficulty()

            if not self.enemies: self.spawn_enemies()
            self.turn_enemies_towards_player()
            self.enemies.draw(screen)
            self.enemies.update()
            self.collision_check()

            draw_crosshair()

    def collision_check(self):
        for bullet in self.player.sprite.bullets:
            bullet_hit_list = pygame.sprite.spritecollide(bullet, self.enemies, True)
            for enemy in bullet_hit_list:
                self.explosions.add(pygame.sprite.GroupSingle(Explosion(enemy.rect.centerx, enemy.rect.centery, 5)))
                self.explosion_sound()
                bullet.kill()
                self.increase_score()
                self.update_difficulty()

        if pygame.sprite.spritecollide(self.player.sprite, self.enemies, False): self.make_game_over()

        for enemy in self.enemies:
            if pygame.sprite.spritecollide(self.player.sprite, enemy.bullets, False): return self.make_game_over()

    def make_game_over(self):
        self.destroy_enemies()
        self.explosions.add(pygame.sprite.GroupSingle(
            Explosion(self.player.sprite.rect.centerx, self.player.sprite.rect.centery, 10)))
        self.explosion_sound()
        self.save_high_score()
        self.paused = True

    def turn_enemies_towards_player(self):
        player_x, player_y = self.player.sprite.rect.x, self.player.sprite.rect.y
        for enemy in self.enemies:
            rel_x, rel_y = player_x - enemy.rect.centerx, player_y - enemy.rect.centery
            enemy.angle = math.degrees(math.atan2(-rel_y, rel_x)) - 270
            original_image = enemy.get_current_image()
            enemy.image = pygame.transform.rotate(original_image, enemy.angle)
            enemy.rect = enemy.image.get_rect(center=enemy.rect.center)

    def spawn_enemies(self):
        for _ in range(self.difficulty):
            random_pos_left = -100, random.randint(-100, SCREEN_HEIGHT + 100)
            random_pos_right = SCREEN_WIDTH + 100, random.randint(-100, SCREEN_HEIGHT + 100)
            random_pos_top = random.randint(-100, SCREEN_WIDTH + 100), -100
            random_pos_bottom = random.randint(-100, SCREEN_WIDTH + 100), SCREEN_HEIGHT + 100
            random_pos = random.choice([random_pos_left, random_pos_right, random_pos_top, random_pos_bottom])

            self.enemies.add(Enemy(random.choice(["small", "medium", "big"]), random_pos[0], random_pos[1]))

    def reset(self):
        self.score = 0
        self.difficulty = 10
        self.player.sprite.reset()

    def destroy_enemies(self):
        self.enemies.empty()

    def increase_score(self):
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score

    def update_difficulty(self):
        if self.score == 10 or self.score == 30 or self.score == 60 or self.score == 100:
            self.difficulty += 1

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

    def show_high_score(self):
        draw_text(SCREEN_WIDTH / 2, 15, "HIGH SCORE: " + str(self.high_score))

    def show_score(self):
        draw_text(SCREEN_WIDTH / 2, 40, "SCORE: " + str(self.score))

    def show_difficulty(self):
        draw_text(SCREEN_WIDTH / 2, 65, "DIFFICULTY: " + str(self.difficulty))

    def show_menu_screen(self):
        font_big = pygame.font.Font('font/dogicapixelbold.ttf', 120)
        font_smaller = pygame.font.Font('font/dogicapixelbold.ttf', 30)

        if self.score > 0:
            draw_text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, "GAME OVER", font_big)
            draw_text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 120, f"YOUR SCORE WAS: {self.score}", font_smaller)
        else:
            draw_text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, "SPACE SHOOTER", font_big)

        draw_text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 120,
                  f"PRESS 'SPACE' TO PLAY {'AGAIN' if self.score > 0 else ''}", font_smaller)

    @staticmethod
    def explosion_sound():
        explosion_sound = mixer.Sound('audio/explosion.wav')
        explosion_sound.set_volume(0.3)
        explosion_sound.play()


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

        if game.paused:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game.reset()
                mixer.music.play(-1)
                game.paused = False
        else:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN):
                game.player.sprite.fire()

    game.update()

    pygame.display.update()
