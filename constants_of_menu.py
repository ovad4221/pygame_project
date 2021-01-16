import pygame
from load_functions import load_image
import tkinter as tk

root = tk.Tk()

WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()

FPS = 500

all_sprites = pygame.sprite.Group()
ground_sprites = pygame.sprite.Group()
bar_sprites = pygame.sprite.Group()
level_sprites = pygame.sprite.Group()
name_sprite = pygame.sprite.Group()
shop_sprite = pygame.sprite.Group()

skin_number = 1
