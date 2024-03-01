import pygame
from utility import load_image

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 900
MOVING_GUN = 15
MOVING_LASER = 40


class Laser(pygame.sprite.Sprite):
    image = load_image("laser.png")

    def __init__(self, pos, k=0, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.origimage = Laser.image
        self.image = Laser.image
        self.rect = self.image.get_rect()
        self.positions = pos
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.angle = 0  # угол, на который повернута пулька относительно вертикальной прямой
        # (отсчитывается по часовой стрелке в градусах)
        self.k = k  # коэффициент наклона прямой dy/dx
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.k:
            self.rect.x += -MOVING_LASER / self.k
        self.rect.y -= 40
