import pygame
import os
import sys
from constans import *
from random import randint


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def get_delta(self):
        return self.dx, self.dy

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


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


class WarShipOrPig(pygame.sprite.Sprite):
    def __init__(self, x, y, cell_size, *group):
        super().__init__(*group)
        self.im_pictures = [pygame.transform.scale(load_image('ship1.jpg', colorkey=-1), (cell_size, cell_size)),
                            pygame.transform.scale(load_image('ship1v.jpg', colorkey=-1), (cell_size, cell_size)),
                            pygame.transform.scale(load_image('ship2.jpg', colorkey=-1), (cell_size, cell_size)),
                            pygame.transform.scale(load_image('ship2v.jpg', colorkey=-1), (cell_size, cell_size))]
        self.image = self.im_pictures[0]
        self.rect = pygame.rect.Rect(x, y, cell_size, cell_size)

        self.left_run = False
        self.right_run = False
        self.up_run = False
        self.down_run = False

        self.v = WIDTH // 15

    def update(self, time):
        if pygame.sprite.spritecollideany(self, ground_sprites):
            self.image = self.im_pictures[2]
        else:
            self.image = self.im_pictures[0]
        if self.left_run and not self.right_run:
            self.rect.x += round(self.v * -1 * time / 1000)
        elif not self.left_run and self.right_run:
            self.rect.x += round(self.v * time / 1000)
        if self.up_run and not self.down_run:
            self.rect.y += round(self.v * -1 * time / 1000)
        elif not self.up_run and self.down_run:
            self.rect.y += round(self.v * time / 1000)


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
        self.board = [list(i.strip()) for i in read_list]

        self.left = 0
        self.top = 0

        self.pers = ''
        self.cell_size = WIDTH // 60
        self.bereg = pygame.transform.scale(load_image('bereg.jpg'), (self.cell_size, self.cell_size))
        self.bereg_gor = pygame.transform.scale(load_image('bereg_gor.jpg'), (self.cell_size, self.cell_size))
        self.more_spok = pygame.transform.scale(load_image('more_spok.jpg'), (self.cell_size, self.cell_size))
        self.pesok = pygame.transform.scale(load_image('pesok.jpg'), (self.cell_size, self.cell_size))
        self.zemlya = pygame.transform.scale(load_image('zemlya.jpg'), (self.cell_size, self.cell_size))

        self.bereg_gor2 = pygame.transform.flip(self.bereg_gor, True, False)
        self.bereg2 = pygame.transform.flip(self.bereg, False, True)

    def render(self, screen):
        x = self.left
        y = self.top
        for i in range(self.h_n):
            for j in range(self.w_n):
                if self.board[i][j] == '~':
                    screen.blit(self.more_spok, (x, y))
                elif self.board[i][j] == 'X':
                    self.pers = WarShipOrPig(x, y, self.cell_size, all_sprites)
                    self.board[i][j] = '~'
                elif self.board[i][j] == '^':
                    screen.blit(self.bereg2, (x, y))
                elif self.board[i][j] == '<':
                    screen.blit(self.bereg_gor, (x, y))
                elif self.board[i][j] == '>':
                    screen.blit(self.bereg_gor2, (x, y))
                elif self.board[i][j] == '_':
                    screen.blit(self.bereg, (x, y))

                elif self.board[i][j] == '#':
                    Ground(x, y, self.pesok, all_sprites, ground_sprites)
                    self.board[i][j] = '+'
                elif self.board[i][j] == '@':
                    Ground(x, y, self.zemlya, all_sprites, ground_sprites)
                    self.board[i][j] = '+'
                x += self.cell_size
            x = self.left
            y += self.cell_size
