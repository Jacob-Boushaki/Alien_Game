import pygame

class Settings:
    """A class to hold all of our settings"""

    def __init__(self):
        """Initialize the game's settings"""
        FONT = pygame.font.SysFont("Consolas", 35)

        """Screen settings"""
        self.width = 1280
        self.height = 720
        self.arena_left = 64
        self.arena_right = 960
        self.bg_color = (255, 255, 255)

        """Ship settings"""
        self.ship_speed = 10
        self.ship_limit = 3 # 3

        """Bullet settings"""
        self.bullet_speed = 5
        self.bullet_width = 7
        self.bullet_height = 16
        self.bullet_color = ("cyan")
        self.bullets_allowed = 15

        # Ray gun charge mechanic
        self.ray_charge = float(100)

        """Alien settings"""
        self.alien_speed = 2.5 #2.5
        self.alien_speed_multiplier = 1.0
        self.fleet_drop_speed = 10

        # fleet direction of 1 represents right;
        # -1 represents left.
        self.fleet_direction = 1

        """Scorekeeping settings"""
        # The delay that the score increments as a function of time in milliseconds
        self.score_delay = 1000
        self.score_d_time_event = pygame.USEREVENT + 1
        self.score_d_time = 5

        """Message settings"""
        self.hit_event = pygame.event.Event(pygame.USEREVENT + 2)
        self.game_over = pygame.event.Event(pygame.USEREVENT + 3)
        self.hit_message = FONT.render(f"Ship Hit!", 1, "white")
        self.game_over_message = FONT.render(f"Game Over!", 1, "white")