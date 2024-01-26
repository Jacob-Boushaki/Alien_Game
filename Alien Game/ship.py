import pygame
from settings import Settings

class Ship:
    """A class to manage the ship"""

    def __init__(self, ai_game):
        """"""

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #load the ship image and get its rectangle
        self.image = pygame.image.load(r"C:\Users\jacob\Desktop\Python programs\Alien Game\ship.bmp")
        self.rect = self.image.get_rect()

        #start each new ship at the bottom of the center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

        #Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flags
        Update the ship's x value, not the rect. make sure the ship
        will remain in the field of view of the screen"""

        if self.moving_right and self.rect.right < self.settings.arena_right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > self.settings.arena_left:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def blitme(self):
        #Draw the ship at its current location
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # Center the ship on the screen
        self.rect.midbottom = self.screen_rect.midbottom
