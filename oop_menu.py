import pygame
import os
import sys
from constans import *
from random import randint


def load_image(name, colorkey=None):
    fullname = os.path.join('data_menu', name)
    # если файл не существует, то выходим
    assert os.path.isfile(fullname)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, image, *group):
        super().__init__(*group)
        self.image = image
        self.rect = pygame.rect.Rect(x, y, *image.get_size())


class Board:
    # создание поля
    def __init__(self, file, load_image):
        read_list = open(file, encoding='utf-8').readlines()
        self.w_n = len(read_list[0]) - 1
        self.h_n = len(read_list)
        self.board = [list(i.lstrip()) for i in read_list]
        self.left = 0
        self.top = 0
        self.cell_size = WIDTH // 60
        self.bereg = pygame.transform.scale(load_image('bereg.jpg'), (self.cell_size, self.cell_size))
        self.bereg_gor = pygame.transform.scale(load_image('bereg_gor.jpg'), (self.cell_size, self.cell_size))
        self.more_spok = pygame.transform.scale(load_image('more_spok.jpg'), (self.cell_size, self.cell_size))
        self.pesok = pygame.transform.scale(load_image('pesok.jpg'), (self.cell_size, self.cell_size))
        self.zemlya = pygame.transform.scale(load_image('zemlya.jpg'), (self.cell_size, self.cell_size))

    def render(self, screen):
        x = self.left
        y = self.top
        for i in range(self.h_n):
            for j in range(self.w_n):
                if self.board[i][j] == '#':
                    Ground(self.cell_size * j, self.cell_size * i, self.pesok, all_sprites, ground_sprites)
                elif self.board[i][j] == '~':
                    screen.blit(self.more_spok, (self.cell_size * j, self.cell_size * i))
                elif self.board[i][j] == '@':
                    Ground(self.cell_size * j, self.cell_size * i, self.zemlya, all_sprites, ground_sprites)
                elif self.board[i][j] == '^':
                    screen.blit(pygame.transform.flip(self.bereg, False, True),
                                (self.cell_size * j, self.cell_size * i))
                elif self.board[i][j] == '<':
                    screen.blit(self.bereg_gor, (self.cell_size * j, self.cell_size * i))
                elif self.board[i][j] == '>':
                    screen.blit(pygame.transform.flip(self.bereg_gor, True, False),
                                (self.cell_size * j, self.cell_size * i))
                elif self.board[i][j] == '_':
                    screen.blit(self.bereg, (self.cell_size * j, self.cell_size * i))
            x += self.cell_size
            x = self.left
            y += self.cell_size

