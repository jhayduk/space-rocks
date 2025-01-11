"""
This file contains a single dictionary, _button_mapping, which contains one entry
per known input controller and is used to map axes and buttons to certain
directions or actions that are then returned by the ControllerInput class.
The key for each entry is the GUID for the controller which should be unique
for each model and can be read with

This dictionary is considered internal to the ControllerInput class code
and is not intended to be used elsewhere.

This file is specific for the space-rocks game.
"""
_button_mapping = {
    "default": {
        "name": "default - used if device guid is not in this table",
        "thrust": {"axis": 1, "name": "Axis 1", "invert": -1}
    },
    "0300e6365e0400003c00000001010000": {
        "name": "Microsoft SideWinder Joystick",
        "thrust": {"axis": 1, "name": "Axis 1", "invert": -1}
    }
}
