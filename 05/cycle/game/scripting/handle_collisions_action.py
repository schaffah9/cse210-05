import constants
from game.casting.actor import Actor
from game.casting.cycle import Cycle
from game.casting.score import Score
from game.scripting.action import Action
from game.shared.point import Point

class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.
    
    The responsibility of HandleCollisionsAction is to handle the situation when one cycle collides with the other, or one cycle collides with its segments, or the game is over.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
    """

    def __init__(self):
        """Constructs a new HandleCollisionsAction."""
        self._is_game_over = False

    def execute(self, cast, script):
        """Executes the handle collisions action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            self._handle_own_collision(cast)
            self._handle_cycle_collision(cast)
            self._handle_game_over(cast)
    
    def _handle_own_collision(self, cast):
        """Sets the game over flag if a cycle collides with its trail.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        score1 = cast.get_first_actor("scores")
        cycle1 = cast.get_first_actor("cycles")
        head1 = cycle1.get_segments()[0]
        trail1 = cycle1.get_segments()[1:]

        score2 = cast.get_second_actor("scores")
        cycle2 = cast.get_second_actor("cycles")
        head2 = cycle2.get_segments()[0]
        trail2 = cycle2.get_segments()[1:]
        
        # cycle1 hits trail1
        for segment in trail1:
            if head1.get_position().equals(segment.get_position()):
                score2.add_points(1)
                self._is_game_over = True

        # cycle2 hits trail2
        for segment in trail2:
            if head2.get_position().equals(segment.get_position()):
                score1.add_points(1)
                self._is_game_over = True

    def _handle_cycle_collision(self, cast):
        """Updates the score and sets the game over flag if the cycles collide.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        score1 = cast.get_first_actor("scores")
        cycle1 = cast.get_first_actor("cycles")
        head1 = cycle1.get_head()
        trail1 = cycle1.get_segments()[1:]
        
        score2 = cast.get_second_actor("scores")
        cycle2 = cast.get_second_actor("cycles")
        head2 = cycle2.get_head()
        trail2 = cycle2.get_segments()[1:]

        # cycle1 hits trail2
        for segment in trail2:
            if head1.get_position().equals(segment.get_position()):
                score2.add_points(1)
                self._is_game_over = True

        # cycle2 hits trail1
        for segment in trail1:
            if head2.get_position().equals(segment.get_position()):
                score1.add_points(1)
                self._is_game_over = True

        # cycles collide head on
        if head1.get_position().equals(head2.get_position()):
            self._is_game_over = True

    def _handle_game_over(self, cast):
        """Shows the 'game over' message and turns the cycles white if the game is over.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:
            # cycle 1 turn white
            cycle1 = cast.get_first_actor("cycles")
            cycle1.set_color(constants.WHITE)
            segments1 = cycle1.get_segments()
            for segment in segments1:
                segment.set_color(constants.WHITE)

            # cycle 2 turn white
            cycle2 = cast.get_second_actor("cycles")
            cycle2.set_color(constants.WHITE)
            segments2 = cycle2.get_segments()
            for segment in segments2:
                segment.set_color(constants.WHITE)

            # game over message
            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y / 2)
            position = Point(x, y)

            message = Actor()
            message.set_text("Game Over!")
            message.set_position(position)
            cast.add_actor("messages", message)

            # winner message
            score1 = cast.get_first_actor("scores")
            score2 = cast.get_second_actor("scores")

            winner = Actor()
            if score1.get_points() > score2.get_points():
                text = 'Player 1 Wins!'
            elif score1.get_points() < score2.get_points():
                text = 'Player 2 Wins!'
            else:
                text = 'It\'s a tie!'
            winner.set_text(text)

            new_y = y + constants.CELL_SIZE
            new_position = Point(x, new_y)
            winner.set_position(new_position)
            cast.add_actor("messages", winner)