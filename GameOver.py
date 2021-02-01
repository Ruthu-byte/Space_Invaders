import pygame.font


class GameOver:
    def __init__(self, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 500, 250
        self.block_color = (0, 0, 0)
        self.text_color = (0, 255, 0)
        self.font = pygame.font.SysFont(None, 50)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.block_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_block(self):
        self.screen.fill(self.block_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)