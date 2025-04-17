# /*===================================
#     Stock Imports
# ====================================*/

import random

# /*===================================
#     Main
# ====================================*/

# ...

class Food():
    def __init__(self, surface, color=(245, 222, 179)):
        self.surface = surface
        self.color = color

        self.cell = None

    def spawn(self, grid_cells, boundary_cells, snake_cells):
        while True:
            new_food_cell = random.choice(grid_cells)
            if new_food_cell not in boundary_cells \
                and new_food_cell not in snake_cells \
                and new_food_cell != self.cell:
                self.cell = new_food_cell
                break
        
        # print(f"Food Cell: {self.cell.index}")

    def draw(self):
        if self.cell is None:
            raise ValueError("Food cell is not set. Call spawn() before draw().")
        self.cell.draw(self.surface, self.color)