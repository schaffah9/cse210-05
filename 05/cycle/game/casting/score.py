import constants
from game.casting.actor import Actor
from game.shared.point import Point

class Score(Actor):
    """
    A record of points made or lost. 
    
    The responsibility of Score is to keep track of the points the player has earned.
    It contains methods for adding and getting points. Client should use get_text() to get a string representation of the points earned.

    Attributes:
        _points (int): The points earned in the game.
        _player_number (int): Unique number identifying the player.
    """
    def __init__(self, number):
        super().__init__()
        self._points = 0
        self._player_number = number
        self._text = f"Player {self._player_number}: {self._points}"
        self.add_points(0)

        if self._player_number == 2:
            x = int(constants.MAX_X)
            position = Point(x - len(self._text) * constants.CELL_SIZE, 0)

            self.set_position(position)

    def add_points(self, points):
        """Adds the given points to the score's total points.
        
        Args:
            points (int): The points to add.
        """
        self._points += points
        text = f"Player {self._player_number}: {self._points}"
        self.set_text(text)

    def get_points(self):
        return self._points
        