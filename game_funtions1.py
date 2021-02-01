import pygame
import sys
from Bullets import Bullet
from time import sleep
from Alien import Alien


def key_down(event, ship, screen, setting, bullets, stats):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets, setting, screen, ship)
        bullet_sound = pygame.mixer.Sound("Sounds/Laser sound.wav")
        bullet_sound.play()
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_KP_ENTER:
        stats.game_active = True


def key_up(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_game(ship, setting, screen, bullets, aliens, stats, play_button, sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            key_down(event, ship, screen, setting, bullets, stats)
        elif event.type == pygame.KEYUP:
            key_up(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_game_button(setting, screen, ship, aliens, bullets, stats, play_button, sb, mouse_x, mouse_y)


def check_game_button(setting, screen, ship, aliens, bullets, stats, play_button, sb, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        click_sound = pygame.mixer.Sound("Sounds/CS.wav")
        click_sound.play()
        setting.initialize_dynamic_setting()
        stats.reset_stats()
        stats.restart = False
        stats.game_active = True
        pygame.mouse.set_visible(False)

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(setting, screen, aliens, ship)
        ship.center_ship()


def screen_update(setting, screen, ship, bullets, aliens, stats, play_button, sb, ):
    screen.fill(setting.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    if not stats.game_active:
        sleep(1)
        play_button.draw_button()

    pygame.display.flip()


def update_bullets(bullets, aliens, setting, ship, screen, stats, sb):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(setting, screen, aliens, ship, bullets, stats, sb)


def check_bullet_alien_collision(setting, screen, aliens, ship, bullets, stats, sb):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        explosion_sound = pygame.mixer.Sound("Sounds/Explosion2.wav")
        explosion_sound.play()
        for aliens in collisions.values():
            stats.score += setting.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(sb, stats)
    if len(aliens) == 0:
        bullets.empty()
        setting.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(setting, screen, aliens, ship)


def fire_bullet(bullets, setting, screen, ship):
    if len(bullets) < setting.bullet_allowed:
        new_bullet = Bullet(setting, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(setting, alien_width):
    available_space_x = setting.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_aliens_y(setting, alien_height, ship_height):
    available_space_y = setting.screen_height - 3 * alien_height - ship_height
    number_aliens_y = int(available_space_y / (2 * alien_height))
    return number_aliens_y


def create_alien(setting, screen, aliens, alien_number, row_number):
    alien = Alien(setting, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(setting, screen, aliens, ship):
    alien = Alien(setting, screen)
    number_aliens_x = get_number_aliens_x(setting, alien.rect.width)
    number_rows = get_number_aliens_y(setting, alien.rect.height, ship.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(setting, screen, aliens, alien_number, row_number)


def check_fleet_edges(setting, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(setting, aliens)
            break


def change_fleet_direction(setting, aliens):
    for alien in aliens.sprites():
        alien.rect.y += setting.drop_speed
    setting.alien_direction *= -1


def ship_hit(setting, screen, bullets, ship, stats, aliens, sb):
    if stats.ships_left > 0:
        stats.ships_left -= 1

        sb.prep_ships()

        aliens.empty()
        bullets.empty()
        death_sound = pygame.mixer.Sound("Sounds/ADS2.wav")
        death_sound.play()
        create_fleet(setting, screen, aliens, ship)
        ship.center_ship()

        sleep(1.5)
    else:
        stats.restart = True
        sleep(1.5)
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_alien_bottom(setting, screen, bullets, ship, aliens, stats, sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(setting, screen, bullets, ship, stats, aliens, sb)
            break


def update_aliens(setting, aliens, ship, screen, bullets, stats, sb):
    check_fleet_edges(setting, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(setting, screen, bullets, ship, stats, aliens, sb)

    check_alien_bottom(setting, screen, bullets, ship, aliens, stats, sb)


def check_high_score(sb, stats):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

