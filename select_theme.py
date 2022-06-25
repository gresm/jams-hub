# select random theme from themes.txt file
from random import choice

with open('themes.txt') as f:
    themes = f.read().splitlines()

theme = choice(themes)

with open('theme.txt', 'w') as f:
    f.write(theme)
