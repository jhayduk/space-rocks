"""
The main file for the space-rocks game/

Notes:
    1. All x and y values are in pixels.
    2. Unless otherwise noted, all time is in milliseconds.

Run with:

pipenv install
pipenv shell
python main.py
"""
import argparse
import pygame
import random

from Background import Background
from ControllerInput import ControllerInput
from Rock import Rock
from Ship import Ship

#
# Parse any arguments passed in
#
parser = argparse.ArgumentParser(description="Run the Space Rocks game.")
parser.add_argument('--show-all-events', action='store_true', help='Show all Pygame events')
args = parser.parse_args()

#
# Init the pygame framework
#
pygame.init()

#
# Set up the game screen
#
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Space Rocks")

#
# Define desired frame rate in frames per second (fps)
# Then calculate how many milliseconds per frame (mpf) would correspond to it
# if the frame rate were hit exactly each time.
#
fps = 55
mpf = (1 / fps) * 1000

#
# Check for joysticks and controllers
#
show_controller_status = False
controller_input = ControllerInput()

#
# Set up game elements
#
# These will be updated and drawn in the order they appear in the elements list
#
elements = []

# ------------
#  Background
# ------------
background = Background(screen)
elements.append(background)

# ------
#  Ship
# ------
ship = Ship(screen.get_rect().centerx, screen.get_rect().centery)
elements.append(ship)

# -------
#  Rocks
# -------
_NUM_STARTING_ROCKS = 10

for index in range(_NUM_STARTING_ROCKS):
    rock = Rock(rock_center_x=random.randint(0, screen.get_width()),rock_center_y=random.randint(0, screen.get_height()))
    elements.append(rock)

#
# Run the game loop
#
clock = pygame.time.Clock()
game_over = False
quit_game = False
while not quit_game:
    dt = clock.tick(fps)

    # Clear the screen
    screen.fill((0, 0, 0))

    all_events = pygame.event.get()

    # Handle game level events
    for event in all_events:
        if args.show_all_events:
            print(event)
        if event.type == pygame.QUIT:
            quit_game = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            show_controller_status = not show_controller_status

    # Update the elements, including element level events
    for element in elements:
        element.update(dt=dt, events=all_events, screen=screen)

    # Check for and handle collisions between objects
    for element in [e for e in elements if e.collidable]:
        other_elements = [e for e in elements if e is not element and e.collidable]
        elements_collided_with_indexes = element.rect.collidelistall(other_elements)
        for element_collided_with_index in elements_collided_with_indexes:
            element.collided_with(other_elements[element_collided_with_index])

    # Draw the elements
    for element in elements:
        element.draw(screen)

    # Draw any debug elements
    if show_controller_status:
        controller_input.show_current_state(screen)

    # Update the display to pick up what was drawn above for this frame
    pygame.display.update()

#
# Quick the game and exit out of the program
#
pygame.quit()
