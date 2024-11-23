import time
from typing import NamedTuple
import keyboard
import mss.models
import numpy as np
import mss
import sys

np.set_printoptions(threshold=sys.maxsize)


class PixelPosition(NamedTuple):
    x: int
    y: int


collision_start_points = (
    PixelPosition(727, 227),
    PixelPosition(719, 247),
)


def get_pixel_value(img_np, pixel_pos: PixelPosition) -> int:
    return img_np[pixel_pos.y][pixel_pos.x]


def get_target_offset_x(img_np: np.ndarray, csp: PixelPosition) -> int:
    offset = 0
    for pixel_value in img_np[csp.y][csp.x + 1 :]:
        offset += 1
        # if it's a black pixel
        if pixel_value[2] == 0 or pixel_value[2] == 6:
            break
    return offset


def main() -> None:
    jump_min_offset = 132
    time.sleep(2)
    print("Starting")
    keyboard.press_and_release("space")
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        while True:
            screenshot = sct.grab(monitor)
            img_np = np.array(screenshot)
            for csp in collision_start_points:
                offset = get_target_offset_x(img_np, csp)

                if offset and offset < jump_min_offset:
                    keyboard.press_and_release("space")
                    print("Jumping")
                    time.sleep(0.1)
                    print("On ground")
                    break
