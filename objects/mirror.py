import pygame
from utility import load_image
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 900
MOVING_GUN = 15
MOVING_LASER = 15


class Mirror(pygame.sprite.Sprite):
    image = load_image("mirror.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Mirror.image
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 500
        # угол, на который повернуто зеркало относительно вертикальной прямой
        # (отсчитывается по часовой стрелке в градусах)
        self.angle = 0
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)