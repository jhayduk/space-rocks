import pygame
import typing

from arcade_tools.GameElement import GameElement
from ControllerInput import ControllerInput

#
# The image of the ship is assumed to be positioned such that the front of the
# ship is on the top of the picture. In other words, the image is assumed to
# be of a ship with an orientation vector of (0, -1) (i.e. ↑)
#
_SHIP_IMAGE_FILE = "./images/ship.png"
_THRUSTER_SPEED_PPM = 0.01


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

        #
        # Grab a local pointer to the singleton ControllerInput object so that
        # it does not need to be re-created everytime the update() method is
        # called.
        #
        self._controller_input = ControllerInput()

        # Initialize the base GameElement class items.
        super().__init__(_SHIP_IMAGE_FILE)

        # Reposition the ship so that the center of if it is at the desired position
        self.rect.center = (ship_center_x, ship_center_y)

        # Set the starting orientation of the ship to be straight up
        self.orientation = pygame.math.Vector2(0, -1)

    @typing.override
    def update(self, dt: int, screen: pygame.Surface = None, **kwargs):
        """
        Update the orientation, velocity and location of the ship for the
        next frame.

        There are expected to be two different ship control options: classic
        and fly-by-wire. The classic ship controls require the player to spin
        the ship in a given direction and then apply the thruster to move. When
        using fly-by-wire controls, the player need only point the joystick
        in the desired direction of movement, and the ship will spin towards
        that direction automatically while applying thrusters.

        The keyboard implements classic controls. The left and right arrows
        rotate the ship counter-clockwise and clockwise respectively, the
        up arrow and/or space bar controls the forward thruster, and the down
        arrow controls the reverse thruster.

        Any attached joystick implements fly-by-wire controls where the x-axis
        rotates the ship (left for counter-clockwise and right for clockwise),
        and the y-axis controls the thruster (forward for the forward thruster
        and back for the reverse thruster).

        :param dt: The number of milliseconds since the last call to update.
                    This is used with any movement calculations to help
                    smooth any jitter in the frame rate.
        :param screen: The screen the ship will be drawn on. This is used to
                        know when the ship goes off the screen This parameter
                        MUST be supplied.
        :param kwargs: Any other optional key word arguments, such as events,
                        are ignored by this method.
        """
        # Check that required parameters have been supplied
        if screen is None:
            raise ValueError(f"A screen parameter MUST be supplied to the {self.__class__.__name__}.update() method")

        #
        # Calculate the new velocity based the thruster value
        #
        # Note that the ship goes faster the longer the thruster is applied.
        #
        self.velocity += self.orientation * (self._controller_input.thrust() * _THRUSTER_SPEED_PPM)

        # Move the ship with the new velocity
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt

    #
    # GameElement's collide_with() and draw() methods are, currently,
    # sufficient for the Background, so it is used as is. These will all
    # be eventually overridden with custom versions for the ship.
    #
