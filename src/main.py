import math
import time

import PyTouchBar.Haptic as Haptic
from pynput import mouse
from PyTouchBar.Haptic import Pattern, Time

# Change these to change the haptics' "feel"
haptic_cooldown = 20  # Min cooldown between haptic bumps
haptic_min_pixel_distance = 10  # Minimum pixels moved before another haptic bump
# https://developer.apple.com/documentation/appkit/nshapticfeedbackmanager/performancetime
haptic_performance = Pattern.generic
# https://developer.apple.com/documentation/appkit/nshapticfeedbackmanager/performancetime
haptic_time = Time.now


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


last_mouse_pos = None
last_haptic_time = None


def on_move(x, y):
    global last_haptic_time
    global last_mouse_pos
    curr = time.time()
    if (
        last_mouse_pos is None
        or distance((x, y), last_mouse_pos) > haptic_min_pixel_distance
    ):
        last_mouse_pos = (x, y)
        if (
            last_haptic_time is None
            or (curr - last_haptic_time) * 1000 > haptic_cooldown
        ):
            Haptic.perform(haptic_performance, haptic_time)
            # print("Pointer moved to {0}".format((x, y)))
            last_haptic_time = curr


with mouse.Listener(
    on_move=on_move,
) as listener:
    listener.join()
