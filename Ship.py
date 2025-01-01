import pygame

from arcade_tools.GameElement import GameElement

#
# The image of the ship is assumed to be positioned such that the front of the
# ship is on the top of the picture. In other words, the image is assumed to
# be of a ship with an orientation vector of (0, -1) (i.e. ↑)
#
_SHIP_IMAGE_FILE = "./images/ship.png"


class Ship(GameElement):
    """
    Ship is a subclass of GameElement, which means it is updatable,
    participates in collisions, and is drawable on the game screen.

    Because it is a GameElement, it has a rect attribute which has x and y
    positions as well as all the standard pygame.rect attributes like
    topleft and center.

    The x and y positions are always defined in pixels and refer to the top
    left corner of the image. The x and y values are always relative to the
    top left corner of the game screen itself, which is defined to be at
    x=0, y=0.

    A Ship also has a velocity which is a Vector2 value in pixels per
    millisecond (ppm), with a unit vector pointing 1 ppm to the right and
    1 ppm down (↘).

    A Ship also has an orientation which changes as the ship rotates. The
    orientation is a unit vector that points in the direction that the front
    of the ship is facing. The thrusters always increase the velocity in the
    direction of the orientation vector.

    Initially, there is only ever one ship in the game. However, this class
    is written to allow for a multiplayer option in the future.
    """
    def __init__(self, ship_center_x: int, ship_center_y: int):
        """

        :param ship_center_x: The x component of the position where the center
                                of the ship should be when first instantiated,
        :param ship_center_y: The y component of the position where the center
                                of the ship should be when first instantiated,
        """
        # Make sure pygame is initialized.
        if not pygame.get_init():
            raise RuntimeError(
                f"Pygame must be initialized before creating a {self.__class__.__name__} object. "
                f"Please call pygame.init() before using this class."
            )

        # Initialize the base GameElement class items.
        super().__init__(_SHIP_IMAGE_FILE)

        # Reposition the ship so that the center of if it is at the desired position
        self.rect.center = (ship_center_x, ship_center_y)

        # Set the starting orientation of the ship to be straight up
        self.orientation = pygame.math.Vector2(0, -1)

    #
    # GameElement's update(), collide_with() and draw() methods are, currently,
    # sufficient for the Background, so it is used as is. These will all
    # be eventually overridden with custom versions for the ship.
    #
