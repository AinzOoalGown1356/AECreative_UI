from gtuner import *  # necessary for get_val and get_actual button presses
from creative_helper import *  # necessary for Combo class and set_val method
import time

combo = Combo()
l3_hold_start = 0  # Initialize start time
holding_l3 = False  # State flag to track L3 hold

def iterate(button_bytes, stick_bytes, **kwargs):  
    global l3_hold_start, holding_l3

    combo.buttons, combo.sticks = button_bytes, stick_bytes
    
    if get_actual(7):  # If LT is pressed 
        combo.set_val(8, 100)  # Hold down L3
        if not holding_l3:  # Start the timer if not already holding L3
            l3_hold_start = time.time()
            holding_l3 = True

    # Check if 5 seconds have passed since L3 was pressed
    if holding_l3 and (time.time() - l3_hold_start >= 5):
        combo.set_val(8, 0)  # Release L3
        holding_l3 = False  # Reset state flag
    
    return combo.buttons, combo.sticks
