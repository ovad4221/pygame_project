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

# size
TILE_WIDTH = 50
TILE_HEIGHT = 50

# pers parameters
MAX_HEALTH = 100

# ememies parameters
MAX_ENEMY_HEALTH = 50

# game parameters
BULLET_SPEED = 5
