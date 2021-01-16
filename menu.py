import pygame
from oop_menu import *
from constants_of_menu import *


class Roles:
    def __init__(self):
        self.count_of_coins = 0
        self.font = pygame.font.Font(None, 30)
        self.text1 = self.font.render("Чтобы начать уровень, нажмите английскую p,", True, (255, 100, 100))
        self.text2 = self.font.render("находясь на нем.", True, (255, 100, 100))
        self.text3 = self.font.render("Чтобы выйти из игры нажмите escape", True, (255, 100, 100))
        self.image_coin = load_image('coin.png', 'data')
        self.screen2 = pygame.Surface(
            [self.text1.get_width(),
             self.image_coin.get_height() +
             + self.text1.get_height() + self.text2.get_height() + self.text3.get_height() + 66])
        self.screen2.fill('black')
        self.screen2.blit(self.image_coin, (0, 0))
        self.screen2.blit(self.text1, (0, self.image_coin.get_height() + 22))
        self.screen2.blit(self.text2, (0, self.image_coin.get_height() + self.text1.get_height() + 44))
        self.screen2.blit(self.text3,
                          (0, self.image_coin.get_height() + self.text1.get_height() + self.text2.get_height() + 66))
        self.font = pygame.font.Font(None, 100)

    def print_rules(self):
        self.coin_count = self.font.render(f"{self.count_of_coins}", True, (255, 100, 100))
        pygame.draw.rect(self.screen2, 'black', (
            self.image_coin.get_width(), 0, self.screen2.get_width() - self.image_coin.get_width(),
            self.coin_count.get_height()))
        self.screen2.blit(self.coin_count, (self.image_coin.get_width() + 10, 0))
        return self.screen2


class NameOfGame(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(name_sprite)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

        self.change = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if not self.change % 50:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        self.change = (self.change + 1) % 50


def start_window():
    screen.fill((0, 0, 0))
    pygame.mixer.music.load(os.path.join('sounds', 'саундтрек.wav'))
    color_play = (100, 255, 100)
    font = pygame.font.Font(None, 300)
    text_play = font.render("Play", True, color_play)
    text_x = WIDTH // 2 - text_play.get_width() // 2
    text_y_play = HEIGHT // 1.5 - text_play.get_height() // 2
    image_name = load_image("заставка спрайты.png", 'data_menu')
    NameOfGame(image_name, 2, 4, WIDTH // 2 - image_name.get_width() // 4, HEIGHT // 2 - image_name.get_height() // 2)
    pygame.mixer.music.play(-1)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if text_x <= event.pos[0] <= text_x + text_play.get_width() and \
                        text_y_play <= event.pos[1] <= text_y_play + text_play.get_height():
                    color_play = (50, 125, 50)
                else:
                    color_play = (100, 255, 100)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if text_x <= event.pos[0] <= text_x + text_play.get_width() and \
                        text_y_play <= event.pos[1] <= text_y_play + text_play.get_height():
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    return run
        text_play = font.render("Play", True, color_play)
        screen.blit(text_play, (text_x, text_y_play))
        name_sprite.update()
        name_sprite.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.display.set_caption('Решение')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    rules = Roles()
    font = pygame.font.Font(None, 100)
    text_winner1 = font.render("Вы прошли игру, поздравляю!", True, (255, 204, 0))
    text_winner2 = font.render("Спасибо за прохождение!", True, (255, 204, 0))
    font = pygame.font.Font(None, 30)
    text_for_developers1 = font.render("Игру разработали:", True, (255, 204, 0))
    text_for_developers_ovad = font.render("Овсянников Андрей;", True, (255, 204, 0))
    text_for_developers_emil = font.render("Галимов Эмиль;", True, (255, 204, 0))
    text_for_developers_anton = font.render("Петрин Антон.", True, (255, 204, 0))

    board = Board('map-obj.txt', load_image)
    board.render(screen)
    for i in level_sprites:
        all_sprites.add(i)
    for i in shop_sprite:
        all_sprites.add(i)
    all_sprites.add(board.pers)
    Barier(board.left, board.top, board.w_n * board.cell_size, board.h_n * board.cell_size, False, False, all_sprites,
           bar_sprites)
    Barier(board.left, board.top, board.w_n * board.cell_size, board.h_n * board.cell_size, True, False, all_sprites,
           bar_sprites)
    Barier(board.left, board.top, board.w_n * board.cell_size, board.h_n * board.cell_size, False, True, all_sprites,
           bar_sprites)
    Barier(board.left, board.top, board.w_n * board.cell_size, board.h_n * board.cell_size, True, True, all_sprites,
           bar_sprites)
    camera = Camera(board.pers.rect.x, board.pers.rect.y)
    clock = pygame.time.Clock()
    level = None
    running = start_window()
    pygame.mouse.set_visible(False)
    pygame.mixer.music.load(os.path.join('sounds', 'фон карты.wav'))
    pygame.mixer.music.play(-1)
    channel1 = pygame.mixer.Channel(0)
    channel2 = pygame.mixer.Channel(1)
    channel3 = pygame.mixer.Channel(2)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    board.pers.up_run = True
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    board.pers.down_run = True
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    board.pers.left_run = True
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    board.pers.right_run = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    board.pers.up_run = False
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    board.pers.down_run = False
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    board.pers.left_run = False
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    board.pers.right_run = False
        all_sprites.update(clock.tick(FPS), channel2)
        camera.update(board.pers)
        board.left += camera.get_delta()[0]
        board.top += camera.get_delta()[1]
        for sprite in all_sprites:
            camera.apply(sprite)
        level = board.pers.level_collide()
        shop = board.pers.shop_collide()
        if level:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                channel1.play(level.sound, loops=-1)
            if pygame.key.get_pressed()[pygame.K_p] and level.ready and not level.passed:
                level.create()
                rules.count_of_coins += level.run()
                if len(board.level_list) - 1 != board.level_list.index(level) and level.passed:
                    board.level_list[board.level_list.index(level) + 1].ready = True
                clock.tick()
                board.pers.all_flags_move_false()
        else:
            if channel1.get_busy():
                channel1.stop()
                pygame.mixer.music.unpause()

        board.render(screen)
        all_sprites.draw(screen)

        if shop:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                channel3.play(shop.sound, loops=-1)
            if pygame.key.get_pressed()[pygame.K_p]:
                rules.count_of_coins = shop.run(WIDTH // 2 - shop.screen2.get_width() // 2,
                         HEIGHT // 2 - shop.screen2.get_height() // 2, screen, rules.count_of_coins)
                board.pers.re_list(board.cell_size)
                board.pers.all_flags_move_false()
        else:
            if channel3.get_busy():
                channel3.stop()
                pygame.mixer.music.unpause()

        screen.blit(rules.print_rules(), (WIDTH // 60, HEIGHT // 60))

        if sum([i.passed for i in level_sprites]) == len(level_sprites):
            screen.blit(text_winner1, (WIDTH // 3.5, HEIGHT // 30))
            screen.blit(text_winner2, (WIDTH // 3.5, HEIGHT // 30 + text_winner1.get_height()))

            screen.blit(text_for_developers1,
                        (WIDTH // 1.2, HEIGHT // 30 + text_winner1.get_height() * 2))
            screen.blit(text_for_developers_ovad,
                        (WIDTH // 1.2, HEIGHT // 30 + text_winner1.get_height() * 2 + text_for_developers1.get_height()))
            screen.blit(text_for_developers_emil,
                        (WIDTH // 1.2,
                         HEIGHT // 30 + text_winner1.get_height() * 2 + text_for_developers1.get_height() * 2))
            screen.blit(text_for_developers_anton,
                        (WIDTH // 1.2,
                         HEIGHT // 30 + text_winner1.get_height() * 2 + text_for_developers1.get_height() * 3))
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
