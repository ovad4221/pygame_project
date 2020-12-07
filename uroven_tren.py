import pygame
from oop_maybe import Person, Log


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Level')
    size = width, height = 600, 600
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    fps = 500
    running = True
    pers = Person(300, 250)
    # дальше мы одно бревно заменяем уже на список бревен из класса уровня
    log = Log((100, 300, 400, 5))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # d down
                if event.key == 100:
                    pers.right_ran = True
                # a down
                elif event.key == 97:
                    pers.left_run = True
                # w down
                if event.key == 119:
                    pers.jump()
                # s down
                if event.key == 115:
                    pers.g += 100
                clock.tick()
            if event.type == pygame.KEYUP:
                # d up
                if event.key == 100:
                    pers.right_ran = False
                # a up
                elif event.key == 97:
                    pers.left_run = False
                # s up
                if event.key == 115:
                    pers.g -= 100
        if log.log_in(pers):
            pers.on_log = True
            pers.jump_v = 0
            pers.y = log.y_u - pers.height
        else:
            pers.on_log = False
        time = clock.tick(fps)
        pers.run(time)
        pers.fly(time)
        pygame.draw.rect(screen, '#ff0000', (int(pers.x), int(pers.y), pers.width, pers.height))
        pygame.draw.rect(screen, log.color, (log.x_l, log.y_u, log.width, log.height))
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
