import pygame
from constans import *


class Person(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__(all_sprites, pers_sprites)
        self.width = int(40 * (WIDTH / 1366))
        self.height = int(60 * (HEIGHT / 768))
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(x, y)
        self.speed = 5
        self.jump_v = 0
        self.g = 0.05
        self.left_run = False
        self.right_ran = False
        # jump_count чтобы нельзя было несколько раз подряд прыгать, и для реализации двойных прыжков
        self.jump_count = 0
        self.health = 100
        self.coins_count = 0

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
            # if pygame.sprite.spritecollide(self, logs_sprites, False, pygame.sprite.collide_mask)[0].tile_type == 1:
            # self.rect = self.rect.move(-speed, 0)
            # elif pygame.sprite.spritecollide(self, logs_sprites, False, pygame.sprite.collide_mask)[0].tile_type == 2 and self.right_ran:
            # self.rect = self.rect.move(0, -speed)
            # elif pygame.sprite.spritecollide(self, logs_sprites, False, pygame.sprite.collide_mask)[0].tile_type == 2 and self.left_run:
            # self.rect = self.rect.move(0, speed)
        if pygame.sprite.spritecollide(self, coins_sprites, True):
            self.coins_count += 1

    def jump(self):
        if self.jump_count == 0:
            self.jump_count += 1
            self.jump_v = -5
            self.rect.y -= 2 * (HEIGHT / 600)

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

        if pygame.sprite.spritecollide(self, coins_sprites, True):
            self.coins_count += 1


class Log(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image, tile_type=1):
        super().__init__(logs_sprites, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.tile_type = tile_type
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(coins_sprites, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Hero(Person):
    def __init__(self, x, y, weapon, armor, heal, ko_heal=1):
        super().__init__(x, y)
        self.weapon = weapon
        self.armor = armor
        self.heal = heal
        self.ko_heal = ko_heal

    def kick(self):
        pass


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
        self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 20)
        self.coin_img = coin_img

    def update(self, pos):
        self.rect.x = pos[0] - WIDTH // 2 + 28
        self.rect.y = pos[1] - HEIGHT // 2 + 42

    def update_info(self, health, coin_count):
        self.image.fill(pygame.Color('black'))
        self.image.blit(self.coin_img, (self.rect.width - self.rect.width // 10,
                                        self.rect.height // 2 - self.coin_img.get_height() // 2))
        pygame.draw.rect(self.image, pygame.Color('red'),
                         (self.rect.width // 20, self.rect.height // 2 - 15, int(health / max_health * 200), 30))
        pygame.draw.rect(self.image, pygame.Color('white'),
                         (self.rect.width // 20, self.rect.height // 2 - 15, 200, 30), 2)
        font = pygame.font.Font(None, 50)
        text = font.render(f"{coin_count}", True, (100, 255, 100))
        text_x = self.rect.width - self.rect.width // 30 - text.get_width()
        text_y = self.rect.height // 2 - text.get_height() // 2
        self.image.blit(text, (text_x, text_y))

