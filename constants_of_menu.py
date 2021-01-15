from ctypes import windll
import pygame
from load_functions import load_image


WIDTH = windll.user32.GetSystemMetrics(0)
HEIGHT = windll.user32.GetSystemMetrics(1)
FPS = 500

all_sprites = pygame.sprite.Group()
ground_sprites = pygame.sprite.Group()
bar_sprites = pygame.sprite.Group()
level_sprites = pygame.sprite.Group()
name_sprite = pygame.sprite.Group()

pygame.mixer.pre_init(44100, -16, 1, 512)
