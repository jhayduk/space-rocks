import pygame
from pygame import Surface
from pygame.transform import scale, smoothscale
from typing import override

from arcade_tools.GameElement import GameElement

_BACKGROUND_IMAGE_FILE="./images/space.png"


class Background(GameElement):
    """
    Background is a GameElement that is expected to be drawn first for each
    frame so that its image is behind every other game element.
    """
    def __init__(self, screen: Surface):
        """
        When instantiated, the __init__method is passed the screen surface so
        that this class can make sure that the image loaded will cover the
        entire area be resizing it if necessary.

        :param screen: The game screen that is to have the background image
                        drawn over it. This is passed in during initialization
                        so that the size of the screen can be determined.
        """
        #
        # Make sure pygame is initialized. Normally, this is expected to be
        # done before elements are created, so issue a warning if it had to
        # be done here.
        #
        if not pygame.get_init():
            print(
                f"WARNING: pygame was not initialized when a {self.__class__.__name__} object was instantiated. It has now been initialized, but pygame.init() should normally be called before instantiating any instances of the {self.__class__.__name__} class.")
            pygame.init()

        #
        # Initialize the base GameElement class
        #
        # This will load the background image.
        #
        super().__init__(_BACKGROUND_IMAGE_FILE, collidable=False)

        #
        # Scale the background image to match the size of the screen.
        try:
            self.image = smoothscale(self.image, screen.get_size())
        except ValueError:
            """
            smoothscale can throw a ValueError for a number of reasons including
            if the original surface is not a 24-bit or 32-bit surface. On the off
            chance this is the issue, try using scale() instead of smoothscale()
            if the latter just failed.
            """
            self.image = scale(self.image, screen.get_size())

    @override
    def update(self, *args, **kargs):
        """
        The Background stays once displayed, so the GameElement update method
        is bypassed.
        """
        pass

    @override
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
