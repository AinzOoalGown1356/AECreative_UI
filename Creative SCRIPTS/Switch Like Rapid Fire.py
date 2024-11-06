from gtuner import *  # necessary for get_val and get_actual button presses
from creative_helper import *  # necessary for Combo class and set_val method

combo = Combo()

# Optimize for the fastest possible input cycle (adjusted for typical game limits)
fire_press_duration = 1  # Minimum duration for button press (in iterations)
fire_release_duration = 1  # Minimum duration for button release (in iterations)
current_cycle = 0  # Counter for the current cycle

def iterate(button_bytes, stick_bytes, **kwargs):
    global current_cycle
    combo.buttons, combo.sticks = button_bytes, stick_bytes

    # Check if button ID 4 (RT) is held by the user
    if get_actual(4):  # If RT is initially pressed by the user
        current_cycle += 1

        # Simulate rapid-fire by pressing and releasing as quickly as possible
        if current_cycle <= fire_press_duration:
            combo.set_val(4, 100)  # Press RT (button ID 4) at full strength (100)
        elif current_cycle <= fire_press_duration + fire_release_duration:
            combo.set_val(4, 0)  # Release RT
        else:
            current_cycle = 0  # Reset cycle to repeat the rapid-fire pattern

    return combo.buttons, combo.sticks
