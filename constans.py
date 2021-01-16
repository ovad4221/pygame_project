import pygame
import tkinter as tk

root = tk.Tk()

WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()

FPS = 100

# sprite groups
all_sprites_lbl = pygame.sprite.Group()
pers_sprites = pygame.sprite.Group()
logs_sprites = pygame.sprite.Group()
enemies_sprites = pygame.sprite.Group()
coins_sprites = pygame.sprite.Group()
interface_sprite = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
health_scale_sprites = pygame.sprite.Group()
water_sprites = pygame.sprite.Group()
SPRITE_GROUPS = [all_sprites_lbl, pers_sprites, logs_sprites,
                 enemies_sprites, coins_sprites, interface_sprite,
                 bullet_sprites, health_scale_sprites, water_sprites]

# size
TILE_WIDTH = 50
TILE_HEIGHT = 50

# pers parameters
MAX_HEALTH = 100
PERS_DAMAGE = 20
MAX_BULLETS_SHOOTED = 20
PERS_SPEED = 6

# ememies parameters
MAX_ENEMY_HEALTH = 50
PERIODICITY_OF_ATTACK = 1000
PERIODICITY_OF_JUMP = 2000
ENEMY_DAMAGE = 20
ENEMY_NUMBER = (10, 16)

# game parameters
BULLET_SPEED = 30
MAX_ENEMIES_ALIVE = 3

# Colours
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 255, 100)
ACTIVE_COLOR = (50, 125, 50)
