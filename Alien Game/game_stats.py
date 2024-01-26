class GameStats:
    """Track statistics for AlienInvasion"""
    def __init__(self, ai_game):
        # Initiaize the stats for the game
        self.settings = ai_game.settings
        self.reset_stats()

        # Start the Alien Invasion game in an active state
        self.game_active = True
        
        # Initialize the scorekeeping
        self.score = 0
        self.aliens_killed = 0
        self.level = 1

    def reset_stats(self):
        # Initialize statistics that can change during the game
        self.ships_left = self.settings.ship_limit