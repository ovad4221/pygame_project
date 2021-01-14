import sys
import os
import pytmx
import pygame


# загружаем tmx файл с уровнем
def load_level(filename):
    filename = "data/" + filename
    assert os.path.isfile(filename)
    tiledmap = pytmx.load_pygame(filename)
    return tiledmap


def load_image(name, name_p, colorkey=None):
    fullname = os.path.join(name_p, name)
    # если файл не существует, то выходим
    try:
        assert os.path.isfile(fullname)
    except AssertionError:
        print(fullname)
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
