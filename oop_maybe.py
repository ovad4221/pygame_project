import pygame
import random
import math
from constans import *


class Person(pygame.sprite.Sprite):
    def __init__(self, image, group):
        super().__init__(all_sprites, group)
        self.width = int(40 * (WIDTH / 1366))
        self.height = int(60 * (HEIGHT / 768))
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5
        self.jump_v = 0
        self.g = 0.05
        # jump_count чтобы нельзя было несколько раз подряд прыгать, и для реализации двойных прыжков
        self.jump_count = 0

    def fly(self):
        if not pygame.sprite.spritecollide(self, logs_sprites, False):
            self.rect = self.rect.move(0, self.jump_v)
            self.jump_v += self.g
            # чтобы не было залипания в верхней точке прыжка увеличиваем ускорение
            if 0 <= abs(self.jump_v) <= 1:
                self.g = 0.5
            else:
                self.g = 0.05
        # если персонаж попал в платформу после прыжка, передвигаем его из нее
        if pygame.sprite.spritecollide(self, logs_sprites, False):
            self.rect = self.rect.move(0, -self.jump_v)
            self.jump_v = 0
            self.jump_count = 0


class Log(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image, tile_type=1):
        super().__init__(logs_sprites, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.tile_type = tile_type
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(coins_sprites, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


class Hero(Person):
    def __init__(self, x, y, group, image, weapon=None, armor=None, ko_heal=1):
        super().__init__(image, group)
        self.rect = self.image.get_rect().move(x, y)
        self.left_run = False
        self.right_ran = False
        self.weapon = weapon
        self.armor = armor
        self.ko_heal = ko_heal
        self.health = 100
        self.coins_count = 0

    def kick(self):
        pass

# изменил немного реализацию бега и прыжков, так как способ со временем не роботает со спрайтами (хз почему)
# теперь на каждый кадр перс смещается на 5 пиксилей
    def run(self):
        if self.left_run and not self.right_ran:
            speed = -self.speed
        elif not self.left_run and self.right_ran:
            speed = self.speed
        else:
            speed = 0
        self.rect = self.rect.move(speed, 0)
        if pygame.sprite.spritecollide(self, logs_sprites, False):
            self.rect = self.rect.move(-speed, 0)
        if pygame.sprite.spritecollide(self, coins_sprites, True, pygame.sprite.collide_mask):
            self.coins_count += 1

    def jump(self):
        if self.jump_count == 0:
            self.jump_count += 1
            self.jump_v = -5
            self.rect.y -= 2 * (HEIGHT / 600)

    def update(self, *args):
        self.fly()
        if pygame.sprite.spritecollide(self, coins_sprites, True):
            self.coins_count += 1


class Enemy(Person):
    def __init__(self, group, image, level_size):
        super().__init__(image, group)
        self.damage = 10
        width = level_size[0]
        height = level_size[1]
        self.rect = self.image.get_rect()
        self.new = True
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(height - self.rect.height)
        self.mask = pygame.mask.from_surface(self.image)
        while self.new and len(group) > 0:
            if (not any([pygame.sprite.collide_mask(self, i) for i in group if i != self])) and\
                    (not any([pygame.sprite.collide_mask(self, i) for i in pers_sprites])) and\
                    (not any([pygame.sprite.collide_mask(self, i) for i in logs_sprites])):
                self.new = False
            else:
                self.rect.x = random.randrange(width - self.rect.width)
                self.rect.y = random.randrange(height - self.rect.height)
                self.mask = pygame.mask.from_surface(self.image)
        self.speed = random.randrange(1, 3)
        self.left_run = True
        self.habitat = self.rect.x
        self.left_run = True
        self.target_found = False
        self.health = 50
        self.health_scale = HealthScale(self)

    def update(self, target):
        self.fly()
        self.health_scale.update_info(self)
        speed = 0
        if self.left_run:
            speed = -self.speed
        elif not self.left_run:
            speed = self.speed
        self.rect = self.rect.move(speed, 0)
        if pygame.sprite.spritecollide(self, logs_sprites, False):
            self.rect = self.rect.move(-speed, 0)
            # self.left_run, self.right_ran = self.right_ran, self.left_run
        if self.habitat - 150 > self.rect.x or self.habitat + 150 < self.rect.x and not self.target_found:
            self.left_run = not self.left_run
        if self.habitat - 150 <= target.rect.x <= self.habitat + 150:
            self.target_found = True
        if self.target_found:
            if target.rect.x > self.rect.x:
                self.left_run = False
            else:
                self.left_run = True

        if self.health <= 0:
            self.kill()


# пуля
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, cursor_x, cursor_y):
        super().__init__(all_sprites, bullet_sprites)
        self.image = pygame.Surface((10, 10))
        pygame.draw.circle(self.image, pygame.Color('blue'), (5, 5), 5)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        alpha = math.atan((cursor_y - y) / (cursor_x - x))
        self.speedx = abs(BULLET_SPEED * math.cos(alpha))
        self.speedy = abs(BULLET_SPEED * math.sin(alpha))
        if y < cursor_y and x > cursor_x:
            self.speedy = -self.speedy
        elif y < cursor_y and x < cursor_x:
            self.speedy = -self.speedy
            self.speedx = -self.speedx
        elif y > cursor_y and x < cursor_x:
            self.speedx = -self.speedx
        self.damage = 20

    def update(self, *args):
        self.rect.x -= self.speedx
        self.rect.y -= self.speedy
        if pygame.sprite.spritecollide(self, logs_sprites, False, pygame.sprite.collide_mask):
            self.kill()
        bullet_target = pygame.sprite.spritecollide(self, enemies_sprites, False, pygame.sprite.collide_mask)
        if bullet_target:
            bullet_target[0].health -= self.damage
            self.kill()


# шкала здоровья врагов
class HealthScale(pygame.sprite.Sprite):
    def __init__(self, owner):
        super().__init__(all_sprites, health_scale_sprites)
        self.image = pygame.Surface((int(0.8 * owner.rect.width), int(0.08 * owner.rect.height)))
        self.rect = self.image.get_rect()
        self.rect.x = owner.rect.x
        self.rect.y = owner.rect.y - int(0.06 * owner.rect.height)

    def update_info(self, owner):
        if owner.health <= 0:
            self.kill()
        self.image.fill(pygame.Color('black'))
        self.rect.x = owner.rect.x + (owner.rect.width - self.rect.width) // 2
        self.rect.y = owner.rect.y - int(0.15 * owner.rect.height)
        pygame.draw.rect(self.image, pygame.Color('green'),
                         (0, 0, int((owner.health / MAX_ENEMY_HEALTH) * self.rect.width), self.rect.height))
        pygame.draw.rect(self.image, pygame.Color('white'), (0, 0, self.rect.width, self.rect.height), 1)





class Weapon:
    def __init__(self, lvl, ko_damage=1, ko_rad=1, chance_critic=0.06):
        self.lvl = lvl
        self.ko_damage = ko_damage
        self.ko_rad = ko_rad
        self.chance_critic = chance_critic

    def kick(self):
        pass

    def mega_kick_1(self):
        pass

    def mega_kick_2(self):
        pass


class Armor:
    def __init__(self, lvl, ko_arm=1, ko_ref=1, chance_def=0.05):
        self.lvl = lvl
        self.ko_arm = ko_arm
        self.chance_def = chance_def
        self.ko_ref = ko_ref

    def refresh(self):
        pass


# для центровки перса сделал класс Камера из последнего урока
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.cam_on = False

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        if self.cam_on:
            obj.rect.x += self.dx
            if type(obj) == Enemy:
                obj.habitat += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        if self.cam_on:
            self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class InfoInterface(pygame.sprite.Sprite):
    def __init__(self, coin_img):
        super().__init__(interface_sprite)
        self.image = pygame.Surface([WIDTH, HEIGHT // 20])
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 20)
        self.coin_img = coin_img

    def update(self, pos):
        self.rect.x = pos[0] - WIDTH // 2 + 28
        self.rect.y = pos[1] - HEIGHT // 2 + 42

    def update_info(self, health, coin_count):
        self.image.fill(pygame.Color('black'))
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.image.blit(self.coin_img, (self.rect.width - self.rect.width // 10,
                                        self.rect.height // 2 - self.coin_img.get_height() // 2))
        pygame.draw.rect(self.image, pygame.Color('red'),
                         (self.rect.width // 20, self.rect.height // 2 - 15, int(health / MAX_HEALTH * 200), 30))
        pygame.draw.rect(self.image, pygame.Color('white'),
                         (self.rect.width // 20, self.rect.height // 2 - 15, 200, 30), 2)
        font = pygame.font.Font(None, 50)
        text = font.render(f"{coin_count}", True, (100, 255, 100))
        text_x = self.rect.width - self.rect.width // 30 - text.get_width()
        text_y = self.rect.height // 2 - text.get_height() // 2
        self.image.blit(text, (text_x, text_y))

