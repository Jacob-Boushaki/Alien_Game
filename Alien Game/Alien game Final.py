#Alien game V3
import sys
import pygame
import time

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

pygame.font.init()
FONT = pygame.font.SysFont("Consolas", 35)

BG = pygame.image.load(r"C:\Users\jacob\Desktop\Python programs\Alien Game\space.jpg")

#import random

#pygame.font.init()

#BG = pygame.image.load("Alien game\space.jpg")

class AlienInvasion:
    #Overall class to manage game assets and behavior

    def __init__(self):
        # Initialize the game, and crete game resources

        pygame.init()
        self.settings = Settings()

        # Initialize the clock and timekeeping
        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.elapsed_time = 0

        # Set a timer to incriment the score by [A] every [B] seconds
        pygame.time.set_timer(self.settings.score_d_time_event, self.settings.score_delay)

        #Tell pygame to determine the size of the screen and set the
        #screen width and height based on the players screen size
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Jacob's Alien Invasion")

        # Create an instance to store the game settings
        self.stats = GameStats(self)

        #Set the background color
        self.bg_color = (10, 50, 130)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # Add in the alien
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game"""

        while True:

            # Run the clock for the game
            self.clock.tick(60)
            self.elapsed_time = time.time() - self.start_time
            
            #self.stats.score += 1
            # Ray gun charge stuff
            if self.settings.ray_charge > 100: self.settings.ray_charge = 100
            self.settings.ray_charge += 0.25 * self.settings.alien_speed_multiplier

            # Call a method to check to see if any keyboard events
            # have occured
            self._check_events()

            # Check to see if the game is still active (ships left)
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self.draw()


    def _check_events(self):
        """Respond to keypresses and mouse events"""
            # Did the player quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
            # Did the player press the right or left arrow key?
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # Did the player stop holding down the arrow key?
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.USEREVENT + 1: # This event gradually increments the score per time
                self.stats.score += self.settings.score_d_time

            elif event.type == pygame.USEREVENT + 2: # SHIP HIT
                self.screen.blit(self.settings.hit_message, (self.settings.width/2 - self.settings.hit_message.get_width()/2,
                                                             self.settings.height/2 - self.settings.hit_message.get_height()/2-200))
                pygame.display.flip()
                time.sleep(3)
                # Decrement the number of ships left
                self.stats.ships_left -= 1

                # Get rid of any remaining aliens and bullets
                self.aliens.empty()
                self.bullets.empty()

                # Create a new fleet and center the ship
                self._create_fleet()
                self.ship.center_ship()

                self.stats.score -= self.settings.score_d_time * 3

            elif event.type == pygame.USEREVENT + 3: # GAME OVER
                self.screen.blit(self.settings.hit_message, (self.settings.width/2 - self.settings.hit_message.get_width()/2,
                                                             self.settings.height/2 - self.settings.hit_message.get_height()/2-200))
                
                self.screen.blit(self.settings.game_over_message, (self.settings.width/2 - self.settings.game_over_message.get_width()/2,
                                                             self.settings.height/2 - self.settings.game_over_message.get_height()/2-100))
                pygame.display.flip()
                self.stats.game_active = False
                time.sleep(5)
                sys.exit()
                
    
    def _check_keydown_events(self, event):
        # Is the key the right arrow or is it the left arrow
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        # Did the player hit the Q key to quit the game?
        elif event.key == pygame.K_q:
            sys.exit()

        # Did the player hit the space bar to shoot a bulet?
        elif event.key == pygame.K_SPACE and self.settings.ray_charge > 10:            
            self._fire_bullet()
            self.settings.ray_charge -= 10

        
    def _check_keyup_events(self,event):
        # did the player stop holding down the arrow keys?

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        # Create a new bullet and add it to the bulets group
        # Limit the number of bullets a player can have at a time
        # by adding a constant to the settings file
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        # Update positions of the bullets and get rid of old bullets
        self.bullets.update()

        # Get rid of bullets that have dissapeared off the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Respond to bullet-alien collisions
        # Check for any bullets that have hit aliens, if so
        # get rid of the bullet and the alien
        if pygame.sprite.groupcollide(self.bullets, self.aliens, True, True):
            self.stats.score += 50
            self.stats.aliens_killed += 1


        # Check to see if the aliens group is empty & if so, 
        # create a new fleet
        if not self.aliens:
            # Destroy any existing bullets and make new fleet
            self.bullets.empty()
            self._create_fleet()
            self.stats.score += 1000
            self.settings.alien_speed_multiplier *= 1.1
            self.stats.level += 1
            # This fixes a bug where the number of alins killed at the end of
            # a level is not a multiple of 50
            if (self.stats.aliens_killed % 50) != 0:
                self.stats.aliens_killed += (50-self.stats.aliens_killed % 50)

    def _update_aliens(self):
        # Update the position of all aliens in the fleet
        # Check if the fleet is at an edge then update the
        # positions of all aliens in the fleet
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()


    # Add a method to create a fleet of Aliens
    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Reset the Ray gun charge
        self.settings.ray_charge = 100
        # Make a single Alien.
        aliens = Alien(self)
        alien_width, alien_height = aliens.rect.size
        # Determine how much space you have on the screen for aliens
        available_space_x = (self.settings.arena_right - self.settings.arena_left) - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (2 * alien_height) - (3 * ship_height))

        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
        
    def _create_alien(self, alien_number, row_number):
        # Create an alien and place it in the row
        aliens = Alien(self)
        alien_width, alien_height = aliens.rect.size
        alien_width = aliens.rect.width
        aliens.x = alien_width + 2 * alien_width * alien_number + self.settings.arena_left
        aliens.rect.x = aliens.x
        aliens.rect.y = alien_height + 2 * aliens.rect.height * row_number
        self.aliens.add(aliens)

    def _check_fleet_edges(self):
        # Respond appropriately if any aliens have reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        # Drop the entire fleet and change direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        # Respond to the ship being hit by an alien
        if self.stats.ships_left > 0:
            pygame.event.post(self.settings.hit_event)

        else:
            pygame.event.post(self.settings.game_over)

    def _check_aliens_bottom(self):
        # Check if any aliens have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break


    def draw(self):
        """Update images on the screen, and flip to the new screen."""
        #Redraw the screen each pass through the loop
        self.screen.blit(BG, (0,0))

        time_text = FONT.render(f"Time: {(round(self.elapsed_time * 10) / 10)} s", 1, "white")
        self.screen.blit(time_text, (1010,36))
        score = FONT.render(f"Score: {self.stats.score}", 1, "white")
        self.screen.blit(score, (1010, 136))
        level = FONT.render(f"level {self.stats.level}", 1, "white")
        self.screen.blit(level, (1010, 236))
        aliens_killed = pygame.font.SysFont("Consolas", 15).render(f"Aliens killed: {self.stats.aliens_killed}", 1, "white")
        self.screen.blit(aliens_killed, (1010, 626))

        for i in range(self.stats.ships_left):
            self.screen.blit(self.ship.image, (1100, 300+(i*70)))
        
        # charge_font = FONT.render(f"{self.settings.ray_charge:.0f}", 1, "white")
        # self.screen.blit(charge_font, (1011, 100))

        # Display the Ray gun charge as a battery on screen
        ray = self.settings.ray_charge
        if ray >= 75:
            battery_color = "cyan"
        elif ray > 40:
            battery_color = "green"
        elif ray > 20:
            battery_color = "yellow"
        elif ray > 10:
            battery_color = "orange"
        else:
            battery_color = "red"

        pygame.draw.rect(self.screen, "black", pygame.Rect(1000, 290, 60, 220))
        pygame.draw.rect(self.screen, "black", pygame.Rect(1020, 510, 20, 15))
        pygame.draw.rect(self.screen, battery_color, pygame.Rect(1011, 300, 40, 2 * self.settings.ray_charge))
        #pygame.draw.rect(self.screen, "black", pygame.Rect(1020, 275, 20, 15))
        #H = 2 * self.settings.ray_charge
        #pygame.draw.rect(self.screen, battery_color, pygame.Rect(1011, (500 - H), 40, H))


        self.ship.blitme()
        
        # Draw bullets on the sreen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw the alien
        self.aliens.draw(self.screen)

        # Arena boundries for Dev purposes
        # pygame.draw.rect(self.screen, "purple", pygame.Rect(self.settings.arena_left - 5, 10, 5, 700))
        # pygame.draw.rect(self.screen, "purple", pygame.Rect(self.settings.arena_right, 10, 5, 700))

        #Make the most recently frawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

quit()