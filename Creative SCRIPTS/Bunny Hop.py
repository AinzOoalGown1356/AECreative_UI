from gtuner import *  # necessary for get_val and get_actual button presses
from creative_helper import *  # necessary for Combo class and set_val method

combo = Combo()

# Parameters for the bunny hop
hop_press_duration = 1  # Minimum duration for button press (in iterations)
hop_release_duration = 1  # Minimum duration for button release (in iterations)
current_cycle = 0  # Counter for the current cycle

def iterate(button_bytes, stick_bytes, **kwargs):
    global current_cycle
    combo.buttons, combo.sticks = button_bytes, stick_bytes

    # Check if button ID 15 (A) is held or toggled for bunny hopping
    if get_actual(15):  # If A is initially pressed by the user
        current_cycle += 1

        # Simulate bunny hop by pressing and releasing A as quickly as possible
        if current_cycle <= hop_press_duration:
            combo.set_val(15, 100)  # Press A (button ID 15) at full strength (100)
        elif current_cycle <= hop_press_duration + hop_release_duration:
            combo.set_val(15, 0)  # Release A
        else:
            current_cycle = 0  # Reset cycle to repeat the hop pattern

    return combo.buttons, combo.sticks
