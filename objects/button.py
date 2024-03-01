import pygame
from utility import load_image
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 900
MOVING_GUN = 15
MOVING_LASER = 15


class Button(pygame.sprite.Sprite):
    """Class used to create a button, use setCords to set
        position of topleft corner. Method pressed() returns
        a boolean and should be called inside the input loop."""

    image = load_image("restart_button.png")

    def __init__(self, name, *group):
        super().__init__(*group)
        self.image = load_image(name)
        self.rect = self.image.get_rect()

    def setCords(self, x, y):
        self.rect.topleft = x, y

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
