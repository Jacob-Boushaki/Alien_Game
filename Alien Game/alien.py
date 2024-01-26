import pygame
from pygame.sprite import Sprite
from settings import Settings

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    
    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load(r"C:\Users\jacob\Desktop\Python programs\Alien Game\alien.bmp")
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)
        
    def check_edges(self):
        #Return True if alien is at edge of screen.
        screen_rect = self.screen.get_rect()
        if self.rect.right >= 960 or self.rect.left <= 64:
            return True
    
    def update(self):
        #Move the alien right or left.
        self.x += ((self.settings.alien_speed * self.settings.alien_speed_multiplier) * self.settings.fleet_direction)
        self.rect.x = self.x