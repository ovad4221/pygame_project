class Person:
    def run(self):
        pass

    def jump(self):
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


class Hero(Person):
    def __init__(self, weapon, armor, heal, ko_heal=1):
        self.weapon = weapon
        self.armor = armor
        self.heal = heal
        self.ko_heal = ko_heal

    def kick(self):
        pass
