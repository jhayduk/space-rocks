import pygame
import random

from arcade_tools.GameElement import GameElement

_ROCK_IMAGE_FILES = [
    "./images/rock-large.png",
    "./images/rock-medium.png",
    "./images/rock-small.png"
]


class Rock(GameElement):
    """
    Rock is a subclass of GameElement, which means it is updatable,
    participates in collisions, and is drawable on the game screen.

    Because it is a GameElement, it has a rect attribute which has x and y
    positions as well as all the standard pygame.rect attributes like
    topleft and center.

    The x and y positions are always defined in pixels and refer to the top
    left corner of the image. The x and y values are always relative to the
    top left corner of the game screen itself, which is defined to be at
    x=0, y=0.

    A Rock also has a velocity which is a Vector2 value in pixels per
    millisecond (ppm), with a unit vector pointing 1 ppm to the right and
    1 ppm down (↘).

    When a Rock is first instantiated, is starts off at a random size (small,
    medium, or large), and at a random location. Each time it gets hit, it
    breaks into multiple smaller rocks. Once the smallest rock is hit, it is
    removed from the game.
    """
    def __init__(self, rock_center_x: int, rock_center_y: int):
        """
        :param rock_center_x: The x component of the position where the center
                                of the rock should be when first instantiated,
        :param rock_center_y: The y component of the position where the center
                                of the rock should be when first instantiated,
        """
        # Make sure pygame is initialized.
        if not pygame.get_init():
            raise RuntimeError(
                f"Pygame must be initialized before creating a {self.__class__.__name__} object. "
                f"Please call pygame.init() before using this class."
            )

        # Initialize the base GameElement class items.
        super().__init__(random.choice(_ROCK_IMAGE_FILES))

        # Reposition the rock so that the center of if it is at the desired position
        self.rect.center = (rock_center_x, rock_center_y)

    #
    # GameElement's update(), collide_with() and draw() methods are, currently,
    # sufficient for the rocks, so it is used as is. These will all
    # be eventually overridden with custom versions for the ship.
    #
