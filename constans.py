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

# size
tile_width = 50
tile_height = 50
