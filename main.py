import pygame
from random import *


class Gun():
    def __init__(self, x, y, corner):
        self.x = x
        self.y = y
        self.corn = corner

    def calculation(self):
        x2 = 395
        y2 = 780
        x3 = 405
        y3 = 780
        h = 70
        self.point1 = 1

    def drawing(self, screen):
        pygame.draw.polygon(screen, pygame.Color('Orange'), [(380, 850), (395, 780), (405, 780), (420, 850)], 0)

class Laser():
    def __init__(self):
        self.mm = 0


# if __name__ == '__main__':
#     pygame.init()
#     size = width, height = 800, 900
#     screen = pygame.display.set_mode(size)
#
#     # формирование кадра:
#     # команды рисования на холсте
#     # ...
#     # ...
#     # смена (отрисовка) кадра:
#     pygame.display.flip()
#     # ожидание закрытия окна:
#     while pygame.event.wait().type != pygame.QUIT:
#         pass
#     # завершение работы:
#     pygame.quit()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Space Defender')
    size = width, height = 800, 900
    screen = pygame.display.set_mode(size)

    for i in range(10000):
        screen.fill(pygame.Color('white'),
                    (random() * width,
                     random() * height, 1, 1))

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        gun = Gun(3, 4, 6)
        gun.drawing(screen)
        #screen.fill((0, 0, 0))
        #pygame.draw.circle(screen, (255, 0, 0), (int(x_pos), 200), 20)
        #x_pos += v * clock.tick() / 1000  # v * t в секундах
        pygame.display.flip()
    pygame.quit()
