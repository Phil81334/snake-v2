# /*===================================
#     Stock Imports
# ====================================*/

import pygame

# /*===================================
#     Main
# ====================================*/

# ...

class Cell:
    def __init__(self, index, x, y, width, height):
        self.x = x
        self.y = y
        self.index = index
        self.width = width
        self.height = height
        self.color = (0, 0, 0)

        self.rect = (x, y, width, height)

    def draw(self, surface, color):
        pygame.draw.rect(surface, color, self.rect)