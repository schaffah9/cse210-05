import random
from game.scripting.action import Action
from game.casting.cycle import Cycle

class DrawActorsAction(Action):
    """
    An output action that draws all the actors.
    
    The responsibility of DrawActorsAction is to draw all the actors.

    Attributes:
        _video_service (VideoService): An instance of VideoService.
    """

    def __init__(self, video_service):
        """Constructs a new DrawActorsAction using the specified VideoService.
        
        Args:
            video_service (VideoService): An instance of VideoService.
        """
        self._video_service = video_service

    def execute(self, cast, script):
        """Executes the draw actors action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        score1 = cast.get_first_actor("scores")
        cycle1 = cast.get_first_actor("cycles")
        segments1 = cycle1.get_segments()

        score2 = cast.get_second_actor("scores")
        cycle2 = cast.get_second_actor("cycles")
        segments2 = cycle2.get_segments()

        if random.normalvariate(0,1) > 1.25:
            cycle1.grow_trail(1)
            cycle2.grow_trail(1)

        messages = cast.get_actors("messages")

        self._video_service.clear_buffer()

        self._video_service.draw_actors(segments1)
        self._video_service.draw_actor(score1)
        self._video_service.draw_actors(messages, True)

        self._video_service.draw_actors(segments2)
        self._video_service.draw_actor(score2)
        self._video_service.draw_actors(messages, True)

        self._video_service.flush_buffer()