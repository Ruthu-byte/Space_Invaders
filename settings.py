class Setting:

    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 500
        self.bg_color = (32, 64, 64)

        # Ship speed
        self.ship_limit = 3

        # Setting for bullets
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (0, 0, 0)
        self.bullet_allowed = 3

        # Alien Speed
        self.drop_speed = 10

        # How fast game speed up
        self.speed_scale = 1.1
        self.score_scale = 1.5
        self.speed_alien = 1.2

        self.initialize_dynamic_setting()

    def initialize_dynamic_setting(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # 1 = right and -1=left
        self.alien_direction = 1

        # Alien Points
        self.alien_points = 50

    def increase_speed(self):
        self.alien_speed_factor *= self.speed_alien
        self.ship_speed_factor *= self.speed_scale
        self.bullet_speed_factor *= self.speed_scale

        self.alien_points = int(self.alien_points * self.score_scale)

        print(self.alien_points)


