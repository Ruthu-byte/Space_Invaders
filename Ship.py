import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, screen, setting):
        super(Ship, self).__init__()
        self.screen = screen
        self.setting = setting

        self.image = pygame.image.load('Images/Steampunk rocket(smaller).bmp')

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.setting.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.setting.ship_speed_factor

        self.rect.centerx = self.center

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx

