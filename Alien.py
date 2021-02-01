import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, setting, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.setting = setting

        self.image = pygame.image.load("Images/alien.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.setting.alien_speed_factor * self.setting.alien_direction)
        self.rect.x = self.x
