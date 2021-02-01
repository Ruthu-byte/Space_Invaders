import pygame
from settings import Setting
from Ship import Ship
import game_funtions1 as gf
from pygame.sprite import Group
from stats import GameStats
from button import Button
from Scoreboard import Scoreboard
from GameOver import GameOver


def run_game():
    pygame.init()
    setting = Setting()
    screen = pygame.display.set_mode((setting.screen_width, setting.screen_height))
    pygame.display.set_caption("Alien Invaders")
    ship = Ship(screen, setting)
    bullets = Group()
    aliens = Group()

    play_button = Button(setting, screen, "Play")

    stats = GameStats(setting)

    sb = Scoreboard(setting, screen, stats)

    g_o = GameOver(screen, "Game Over")

    gf.create_fleet(setting, screen, aliens, ship)

    while True:
        gf.check_game(ship, setting, screen, bullets, aliens, stats, play_button, sb)
        gf.screen_update(setting, screen, ship, bullets, aliens, stats, play_button, sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, setting, ship, screen, stats, sb)
            gf.update_aliens(setting, aliens, ship, screen, bullets, stats, sb)
            gf.screen_update(setting, screen, ship, bullets, aliens, stats, play_button, sb)


run_game()
