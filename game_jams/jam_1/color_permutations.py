from __future__ import annotations

from typing import Callable
from random import randint, shuffle


def simple_color_iter(r: int, g: int, b: int, c: bool) -> tuple[int, int, int, bool]:
    # This function is used to iterate through all possible colors smoothly.
    # It is used in the MainMenu class.
    # Increment r by 1 until it is 255, then increment g by 1 and decrement r by 1.
    # Increment g by 1 until it is 255, then increment b by 1 and decrement g by 1.
    # Increment b by 1 until it is 255, then increment r by 1 and decrement b by 1.
    # Return the new color.
    if c:
        if r < 255:
            r += 1
        elif g < 255:
            g += 1
            c = False
        elif b < 255:
            b += 1
            r = 0
            g = 0
        else:
            r = 0
            g = 0
            b = 0
    else:
        if r > 0:
            r -= 1
        elif g < 255:
            g += 1
            c = True
        elif b < 255:
            b += 1
            r = 0
            g = 0
        else:
            r = 0
            g = 0
            b = 0
            c = True
    return r, g, b, c


def color_iter(r: int = -1, g: int = -1, b: int = -1) -> Callable[[], tuple[int, int, int]]:
    c = True
    r = randint(0, 255) if r == -1 else r
    g = randint(0, 255) if g == -1 else g
    b = randint(0, 255) if b == -1 else b
    seq = [0, 1, 2]
    shuffle(seq)

    def internal_color_iter():
        nonlocal c, r, g, b
        r, g, b, c = simple_color_iter(r, g, b, c)
        ret = [0, 0, 0]
        ret[seq[0]] = r
        ret[seq[1]] = g
        ret[seq[2]] = b
        return ret[0], ret[1], ret[2]

    return internal_color_iter
