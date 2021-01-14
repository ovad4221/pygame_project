from ctypes import windll
import pygame


WIDTH = windll.user32.GetSystemMetrics(0)
HEIGHT = windll.user32.GetSystemMetrics(1)
FPS = 500
all_sprites = pygame.sprite.Group()
ground_sprites = pygame.sprite.Group()
bar_sprites = pygame.sprite.Group()
