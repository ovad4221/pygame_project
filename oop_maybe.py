import pygame


class Person:
    def __init__(self, x, y):
        self.rv = 100
        self.lv = -100
        self.width = 35
        self.height = 50
        self.x = x
        self.y = y
        self.jump_v = 0
        self.g = 55
        self.on_log = True
        self.left_run = False
        self.right_ran = False
        self.left_log = False
        self.right_log = False

    def run(self, time):
        if self.left_run and not self.right_ran and not self.left_log:
            speed = self.lv
        elif not self.left_run and self.right_ran and not self.right_log:
            speed = self.rv
        else:
            speed = 0
        self.x += speed * time / 1000

    def jump(self):
        if self.on_log:
            self.jump_v = -75
            self.y -= 3
            self.on_log = False

    def fly(self, time):
        if not self.on_log:
            self.y += self.jump_v * time / 1000
            self.jump_v += self.g * time / 1000

    def draw(self, screen):
        pygame.draw.rect(screen, '#ff0000', (int(self.x), int(self.y), self.width, self.height))


class Log:
    def __init__(self, rect, color='#646423'):
        self.x_l = rect[0]
        self.y_u = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.color = color

    def log_in(self, pers):
        if (0 <= self.y_u - pers.y - pers.height < 2 and
                (self.x_l < pers.x + pers.width and self.x_l + self.width > pers.x)):
            return True
        return False

    # проверка на столкновение с доской. Возвращает 'r', 'l', 'u'.
    def log_knock(self, pers):
        if (0 <= self.x_l - pers.x - pers.width < 2) and True:
            return 'r'
        return -1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x_l, self.y_u, self.width, self.height))


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
