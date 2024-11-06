from gtuner import *  # necessary for get_val and get_actual button presses
from creative_helper import *  # necessary for Combo class and set_val method

combo = Combo()

# Variables for tracking the state of the press cycle
initial_press_detected = False
holding = False

def iterate(button_bytes, stick_bytes, **kwargs):
    global initial_press_detected, holding
    combo.buttons, combo.sticks = button_bytes, stick_bytes

    # Check if button ID 16 is pressed to stop the loop and exit
    if get_actual(16):
        initial_press_detected = False  # Stop the loop
        holding = False  # Reset holding state
        combo.set_val(4, 0)  # Ensure R2 is released
        return combo.buttons, combo.sticks

    # Check if button ID 4 (RT) is pressed initially by the user to start the loop
    if get_actual(4) and not initial_press_detected:
        initial_press_detected = True  # Start the loop after the first press

    # If the initial press has been detected, run the infinite loop of press and release
    if initial_press_detected:
        if not holding:
            combo.set_val(4, 100)  # Hold R2 at full strength
            holding = True  # Set holding state
        else:
            combo.set_val(4, 0)  # Release R2
            holding = False  # Reset holding state to press again

    return combo.buttons, combo.sticks
