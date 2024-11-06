from gtuner import *  # necessary for get_val and get_actual button presses
from creative_helper import *  # necessary for Combo class and set_val method

combo = Combo()

def iterate(button_bytes, stick_bytes, **kwargs):
    combo.buttons, combo.sticks = button_bytes, stick_bytes

    # Constantly pull the left stick's Y-axis (ID 24) back to the maximum (full down position)
    combo.set_val(24, 100)  # Set to maximum down position



    return combo.buttons, combo.sticks
