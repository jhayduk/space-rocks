import pygame
import typing

from arcade_tools.GameElement import GameElement

_BACKGROUND_IMAGE_FILE = "./images/space.png"


class Background(GameElement):
    """
    Background is a GameElement that is expected to be drawn first for each
    frame so that its image is behind every other game element.
    """
    def __init__(self, screen: pygame.Surface):
        """
        When instantiated, the __init__method is passed the screen surface so
        that this class can make sure that the image loaded will cover the
        entire area be resizing it if necessary.

        :param screen: The game screen that is to have the background image
                        drawn over it. This is passed in during initialization
                        so that the size of the screen can be determined.
        """
        # Make sure pygame is initialized.
        if not pygame.get_init():
            raise RuntimeError(
                f"Pygame must be initialized before creating a {self.__class__.__name__} object. "
                f"Please call pygame.init() before using this class."
            )

        #
        # Initialize the base GameElement class
        #
        # This will load the background image.
        #
        super().__init__(_BACKGROUND_IMAGE_FILE, collidable=False)

        #
        # Scale the background image to match the size of the screen.
        try:
            self.image = pygame.transform.smoothscale(self.image, screen.get_size())
        except ValueError:
            """
            pygame.transform.smoothscale can throw a ValueError for a number
            of reasons including if the original surface is not a 24-bit or
            32-bit surface. On the off-chance this is the issue, try using
            pygame.transform.scale() instead of pygame.transform.smoothscale()
            if the latter just failed.
            """
            self.image = pygame.transform.scale(self.image, screen.get_size())

    @typing.override
    def update(self, *args, **kwargs):
        """
        The Background stays once displayed, so the GameElement update method
        is bypassed.
        """
        pass

    @typing.override
    def collided_with(self, other_element: GameElement):
        """
        The Background does not participate in collision detection, so this
        is bypassed.
        """
        pass

    #
    # GameElement's draw() method is sufficient for the Background, so it
    # is used as is.
    #
