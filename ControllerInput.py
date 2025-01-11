import pygame

from controller_config import _button_mapping


class ControllerInput:
    """
    ControllerInput

    This class is intended to capture controller input from the user in a unified
    manner so there is one place from which to get information about what the user
    is trying to do, regardless of the method (e.g. keyboard, joystick, trackball)
    being used.

    This class is a singleton so that it can be accessed from multiple locations
    without having to pass the single instance around everywhere.

    This class is specific for the space-rocks game.
    """
    # The single instance of this class. This is intended to be used internally only.
    _instance = None

    #
    # A flag to make sure that later calls do not reset anything.
    # This is intended to be used internally only.
    #
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not self._is_initialized:
            # Make sure pygame is initialized.
            if not pygame.get_init():
                raise RuntimeError(
                    f"Pygame must be initialized before creating a {self.__class__.__name__} object. "
                    f"Please call pygame.init() before using this class."
                )

            #
            # Now initialize the _joysticks list.
            #
            self._joysticks = []
            num_joysticks = pygame.joystick.get_count()
            if pygame.joystick.get_count() > 0:
                print(f"Found {num_joysticks} joystick{'s' if num_joysticks > 1 else ''}")
                for joystick_id in range(num_joysticks):
                    joystick = pygame.joystick.Joystick(joystick_id)
                    self._joysticks.append(joystick)
                    print(f"  Joystick {joystick_id}")
                    print(f"    Name: {joystick.get_name()}")
                    print(f"    GUID: {joystick.get_guid()}")
                    print(f"    Number of axis: {joystick.get_numaxes()}")
                    print(f"    Number of buttons: {joystick.get_numbuttons()}")
                    print(f"    Number of hats: {joystick.get_numhats()}")
                    print(f"    Number of balls: {joystick.get_numballs()}")

                    #
                    # Check the validity of the config here so that later code
                    # does not have to constantly do it.
                    #
                    guid = joystick.get_guid()
                    known_guid = False
                    if guid in _button_mapping:
                        known_guid = True
                        button_mapping = _button_mapping[guid]
                    else:
                        button_mapping = _button_mapping["default"]

                    #
                    # Pre-fill the start of an error message should an entry in the
                    # controller file not be complete. This part records if the GUID
                    # was found or not. It is expected that the message would be
                    # added to before getting used in a raise RuntimeError() statement.
                    #
                    error_message = ""
                    if known_guid:
                        error_message += f'The joystick with the GUID "{guid}" has an entry in the controller_config.py file but it'
                    else:
                        error_message += f'The joystick with the GUID "{guid}" does not have an entry in controller_config.py file and the entry for the "default" GUID'

                    if "thrust" not in button_mapping:
                        error_message += ' does not have an "thrust" entry in it.'
                        raise RuntimeError(error_message)

                    if "axis" not in button_mapping["thrust"]:
                        error_message += ' does not have an "axis" entry in its "thrust" entry.'
                        raise RuntimeError(error_message)

                    if "invert" not in button_mapping["thrust"]:
                        error_message += ' does not have an "invert" entry in its "thrust" entry.'
                        raise RuntimeError(error_message)


            self._is_initialized = True

    def thrust(self) -> float:
        """
        The amount that the keyboard or any connected joysticks are being
        moved in either the up or down direction for a keyboard, or the
        forward and backward direction for a joystick.

        Multiple devices are handled by adding the values together. This means
        that, technically, the total thrust can range from
        [-num_devices, num_devices]. In practice, it is expected that only
        one y-axis is being manipulated at a time. Just in case, the output of
        this method is clipped so that it stays in the range of [-1.0, 1.0].

        Positive thrust is in the same direction as the ships orientation
        (i.e. the forward thruster provides positive thrust), while negative
        thrust in 180 degrees from the ship's orientation (i.e. the reverse
        thruster provides negative thrust).

        :return: float - The amount of thrust being indicated by all the input
                            devices combined. Positive thrust is in the
                            direction of the ship's orientation. Negative
                            thrust is in the opposite direction.
        :return:
        """
        total_thrust = 0.0

        #
        # First, address the keyboard
        #
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            total_thrust += 1.0
        if keys[pygame.K_DOWN]:
            total_thrust -= 1.0

        #
        # Now, look at any joysticks.
        #
        for joystick in self._joysticks:
            guid = joystick.get_guid()
            if guid in _button_mapping:
                button_mapping = _button_mapping[guid]
            else:
                button_mapping = _button_mapping["default"]
            total_thrust += joystick.get_axis(button_mapping["thrust"]["axis"]) * button_mapping["thrust"]["invert"]

        #
        # Finally, clip the resulting total_thrust value so that is in the range [-1.0, 1.0],
        # and then return it/
        #
        total_thrust = max(-1.0, min(1.0, total_thrust))

        return total_thrust

    def show_current_state(self, screen: pygame.Surface):
        """
        This is meant for debugging only.

        The idea is to display all the relevant keys and axes. It
        might be interesting if the display were overlaid on the game screen
        so that it is easier to see changes and so that writing text on
        the screen can be worked on.
        """
        text_lines = []

        # Keyboard
        keys = pygame.key.get_pressed()
        text_lines.append(f"Keyboard:")
        text_lines.append(f"  Left Arrow: {keys[pygame.K_LEFT]}")
        text_lines.append(f"  Right Arrow: {keys[pygame.K_RIGHT]}")

        # Joysticks
        for joystick in self._joysticks:
            text_lines.append(f"Joystick {joystick.get_id()}")
            text_lines.append(f"  Name: {joystick.get_name()}")
            text_lines.append(f"  GUID: {joystick.get_guid()}")
            for axis in range(joystick.get_numaxes()):
                text_lines.append(f"  Axis {axis}: {joystick.get_axis(axis)}")
            for button in range(joystick.get_numbuttons()):
                text_lines.append(f"  Button {button}: {joystick.get_button(button)}")

        # Draw the text lines
        font_size = 24
        font = pygame.font.SysFont(None, font_size)
        line_position = (10, 10)
        for text_line in text_lines:
            text_surface = font.render(text_line, True, (255, 255, 255))
            screen.blit(text_surface, line_position)
            line_position = (line_position[0], line_position[1] + font_size)
            if line_position[1] + font_size + 10 >= screen.get_height():
                line_position = (screen.get_width() // 2, 10)
