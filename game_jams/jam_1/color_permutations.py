from __future__ import annotations
import random as rd


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


def color_iter() -> callable[[], tuple[int, int, int]]:
    c = True
    r = rd.randint(0, 255)
    g = rd.randint(0, 255)
    b = rd.randint(0, 255)
    seq = [0, 1, 2]
    rd.shuffle(seq)

    def internal_color_iter():
        nonlocal c, r, g, b
        r, g, b, c = simple_color_iter(r, g, b, c)
        ret = [0, 0, 0]
        ret[seq[0]] = r
        ret[seq[1]] = g
        ret[seq[2]] = b
        return tuple(ret)

    return internal_color_iter
