from ctypes import windll
import pygame

WIDTH = windll.user32.GetSystemMetrics(0)
HEIGHT = windll.user32.GetSystemMetrics(1)
FPS = 100

# sprite groups
all_sprites = pygame.sprite.Group()
pers_sprites = pygame.sprite.Group()
logs_sprites = pygame.sprite.Group()
enemies_sprites = pygame.sprite.Group()
coins_sprites = pygame.sprite.Group()
interface_sprite = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
health_scale_sprites = pygame.sprite.Group()
SPRITE_GROUPS = [all_sprites, pers_sprites, logs_sprites,
                 enemies_sprites, coins_sprites, interface_sprite,
                 bullet_sprites, health_scale_sprites]

# size
TILE_WIDTH = 50
TILE_HEIGHT = 50

# pers parameters
MAX_HEALTH = 100
PERS_DAMAGE = 20

# ememies parameters
MAX_ENEMY_HEALTH = 50
PERIODICITY_OF_ATTACK = 1000
ENEMY_DAMAGE = 100

# game parameters
BULLET_SPEED = 5

# Colours
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 255, 100)
ACTIVE_COLOR = (50, 125, 50)
