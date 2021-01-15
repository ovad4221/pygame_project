import pygame
import random
import math
from constans import *


class Person(pygame.sprite.Sprite):
    def __init__(self, group, sheet, columns, rows):
        super().__init__(all_sprites, group)
        self.width = int(40 * (WIDTH / 1366))
        self.height = int(60 * (HEIGHT / 768))
        # self.image = pygame.transform.scale(image, (self.width, self.height))
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 3
        self.jump_v = 0
        self.g = 0.05
        # jump_count чтобы нельзя было несколько раз подряд прыгать, и для реализации двойных прыжков
        self.jump_count = 0
        self.clock = pygame.time.Clock()
        self.time = 0
        self.left_run = False
        self.right_run = False
        self.health = 100
        self.dead = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

        for i in range(len(self.frames)):
            self.frames[i] = self.frames[i].convert_alpha()

    def fly(self):
        if not self.dead:
            if not pygame.sprite.spritecollide(self, logs_sprites, False, pygame.sprite.collide_mask):
                self.rect = self.rect.move(0, self.jump_v)
                self.jump_v += self.g
                # чтобы не было залипания в верхней точке прыжка увеличиваем ускорение
                if 0 <= abs(self.jump_v) <= 1:
                    self.g = 0.5
                else:
                    self.g = 0.05
            # если персонаж попал в платформу после прыжка, передвигаем его из нее
            if pygame.sprite.spritecollide(self, logs_sprites, False, pygame.sprite.collide_mask):
                self.rect = self.rect.move(0, -self.jump_v)
                self.jump_v = 0
                self.jump_count = 0

    def new_frame(self):
        self.time += self.clock.tick()
        if self.health <= 0 and not self.dead:
            self.dead = True
            self.time = 0
        elif self.dead:
            self.cur_frame = 9
            self.image = self.frames[self.cur_frame]
        elif self.jump_count == 1:
            self.cur_frame = 6
            self.image = self.frames[self.cur_frame]
            if self.left_run:
                self.image = pygame.transform.flip(self.image, True, False)
        elif self.time >= 200 and self.right_run:
            self.cur_frame = (self.cur_frame + 1) % 4 + 1
            self.time = 0
            self.image = self.frames[self.cur_frame]
        elif self.time >= 200 and self.left_run:
            self.cur_frame = (self.cur_frame + 1) % 4 + 1
            self.time = 0
            self.image = pygame.transform.flip(self.frames[self.cur_frame], True, False)
        elif not self.left_run and not self.right_run:
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]

    def jump(self):
        if self.jump_count == 0 and not self.dead:
            self.jump_count += 1
            self.jump_v = -5
            self.rect.y -= 2 * (HEIGHT / 600)


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
    def __init__(self, x, y, group, sheet, columns, rows, weapon=None, armor=None, ko_heal=1):
        super().__init__(group, sheet, columns, rows)
        self.rect = self.image.get_rect().move(x, y)
        self.weapon = weapon
        self.armor = armor
        self.ko_heal = ko_heal
        self.health = 100
        self.coins_count = 0
        self.game_over = False

    def kick(self, pos):
        self.weapon.kick(self, pos)

# изменил немного реализацию бега и прыжков, так как способ со временем не роботает со спрайтами (хз почему)
# теперь на каждый кадр перс смещается на self.speed пиксилей
    def run(self):
        if not self.dead:
            if self.left_run and not self.right_run:
                speed = -self.speed
            elif not self.left_run and self.right_run:
                speed = self.speed
            else:
                speed = 0
            self.rect = self.rect.move(speed, 0)
            if pygame.sprite.spritecollide(self, logs_sprites, False, pygame.sprite.collide_mask):
                self.rect = self.rect.move(-speed, 0)
            if pygame.sprite.spritecollide(self, coins_sprites, True, pygame.sprite.collide_mask):
                self.coins_count += 1

    def update(self, *args):
        self.fly()
        if pygame.sprite.spritecollide(self, coins_sprites, True):
            self.coins_count += 1
        if self.dead and self.time >= 1000:
            self.kill()
            self.game_over = True
        self.new_frame()


class Enemy(Person):
    def __init__(self, group, sheet, columns, rows, level_size):
        super().__init__(group, sheet, columns, rows)
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
        self.habitat = self.rect.x
        self.left_run = True
        self.right_run = False
        self.target_found = False
        self.health = 50
        self.health_scale = HealthScale(self)
        self.attack_timer = 0
        self.jump_timer = 0
        self.clock_for_actions = pygame.time.Clock()

    def update(self, target):
        self.fly()
        # обновляем шкалу здоровья
        self.health_scale.update_info(self)
        dt = self.clock_for_actions.tick()
        speed = 0
        # логика движения
        if self.left_run and not self.right_run:
            speed = -self.speed
        elif not self.left_run and self.right_run:
            speed = self.speed
        self.rect = self.rect.move(speed, 0)
        if pygame.sprite.spritecollide(self, logs_sprites, False, pygame.sprite.collide_mask):
            self.rect = self.rect.move(-speed, 0)
        # если нет цели, ходит туда-сюда
        if not self.target_found:
            if self.habitat - 150 > self.rect.x or self.habitat + 150 < self.rect.x:
                self.left_run = not self.left_run
                self.right_run = not self.right_run
        # если есть, начинает преследовать ее
        if self.habitat - 150 <= target.rect.x <= self.habitat + 150:
            self.target_found = True

        self.jump_timer += dt
        if self.target_found:
            if self.rect.x - 10 < target.rect.x < self.rect.x + 10:
                self.left_run = False
                self.right_run = False
            elif self.rect.x - 10 > target.rect.x:
                self.left_run = True
                self.right_run = False
            elif self.rect.x + 10 < target.rect.x:
                self.left_run = False
                self.right_run = True

            if target.rect.y < self.rect.y and self.jump_timer >= PERIODICITY_OF_JUMP:
                self.jump()
                self.jump_timer = 0
        # раз в некоторые промеуток времени - атака цели
        self.attack_timer += dt
        if self.attack_timer >= PERIODICITY_OF_ATTACK:
            if self.target_found:
                self.attack(target)
                self.attack_timer = 0

        if self.dead and self.time > 500:
            self.kill()
        self.new_frame()

    def attack(self, target):
        if not target.dead:
            Bullet(self.rect.x + self.rect.width // 2, self.rect.y + 10,
                   target.rect.x, target.rect.y + 10, self, ENEMY_DAMAGE)


# пуля
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, cursor_x, cursor_y, owner, damage):
        super().__init__(all_sprites, bullet_sprites)
        self.image = pygame.Surface((10, 10))
        pygame.draw.circle(self.image, pygame.Color('yellow'), (5, 5), 5)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        # скорости по х и по у
        try:
            alpha = math.atan((cursor_y - y) / (cursor_x - x))
            self.speedx = abs(BULLET_SPEED * math.cos(alpha))
            self.speedy = abs(BULLET_SPEED * math.sin(alpha))
            if y <= cursor_y and x >= cursor_x:
                self.speedy = -self.speedy
            elif y <= cursor_y and x <= cursor_x:
                self.speedy = -self.speedy
                self.speedx = -self.speedx
            elif y >= cursor_y and x <= cursor_x:
                self.speedx = -self.speedx
        except ZeroDivisionError:
            self.kill()
        self.damage = damage
        self.owner = owner

    def update(self, *args):
        self.rect.x -= self.speedx
        self.rect.y -= self.speedy
        if pygame.sprite.spritecollide(self, logs_sprites, False, pygame.sprite.collide_mask):
            self.kill()
        bullet_target = pygame.sprite.spritecollide(self, enemies_sprites, False, pygame.sprite.collide_mask)
        if bullet_target:
            if type(bullet_target[0]) != type(self.owner):
                bullet_target[0].health -= self.damage
                self.kill()

        bullet_target = pygame.sprite.spritecollide(self, pers_sprites, False, pygame.sprite.collide_mask)
        if bullet_target:
            if type(bullet_target[0]) != type(self.owner):
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
    def __init__(self, ko_damage=1, ko_rad=1, chance_critic=0.06):
        self.ko_damage = ko_damage
        self.ko_rad = ko_rad
        self.chance_critic = chance_critic

    def kick(self, owner, pos):
        if len(bullet_sprites) < 10:
            Bullet(owner.rect.x + owner.rect.width // 2, owner.rect.y + 10, pos[0], pos[1], owner, PERS_DAMAGE)

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

