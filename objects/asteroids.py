import pygame
import random

from utility import load_image

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 900
MOVING_GUN = 15
MOVING_LASER = 15


class Asteroids(pygame.sprite.Sprite):
    image = load_image("asteroids.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Asteroids.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOW_WIDTH)
        self.rect.y = random.randrange(100, WINDOW_HEIGHT - 300)
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)