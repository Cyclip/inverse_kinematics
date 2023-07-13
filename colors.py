from typing import *
import colorsys

def gen_colours(base_red: Tuple[int, int, int], n: int) -> List[Tuple[int, int, int]]:
    # Convert base_red to HSV
    r, g, b = base_red
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)

    # Calculate the step size for changing the hue
    hue_step = 1 / n

    rainbow_colors = []

    # Generate rainbow colors
    for i in range(n):
        # Update the hue value
        hue = (h + i * hue_step) % 1

        # Convert the hue back to RGB
        r1, g1, b1 = colorsys.hsv_to_rgb(hue, s, v)

        # Apply base red to the rainbow colors
        r2 = int(r1 * 255)
        g2 = int(g1 * 255)
        b2 = int(b1 * 255)

        rainbow_colors.append((r2, g2, b2))

    return rainbow_colors