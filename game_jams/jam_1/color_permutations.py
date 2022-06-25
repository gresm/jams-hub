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
