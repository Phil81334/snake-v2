# /*===================================
#     Stock Imports
# ====================================*/

# ...

# /*===================================
#     Main
# ====================================*/

from models.direction_enum import SnakeDirectionEnum

class Snake():
    def __init__(self, surface, size=5, speed=500, color=(0, 255, 0)):
        self.surface = surface
        self.size = size
        self.speed = speed
        self.color = color

        self.current_cell = None
        self.cells = []
        self.last_snake_update_time = 0
        self.current_direction = SnakeDirectionEnum.RIGHT
        self.collided = False
        self.food_eaten = False

    def spawn(self, cells):
        self.cells = cells
        self.current_cell = self.cells[0]

    def move(self, directions_queue, grid_cells, grid_cols, boundary_cells, food, current_time):
        if current_time - self.last_snake_update_time < self.speed:
            return
    
        # Determine direction
        if directions_queue:
            self.current_direction = directions_queue[0]
            if len(directions_queue) > 1:
                directions_queue.pop(0)
    
        # Get new head index
        head = self.cells[-1]
        if self.current_direction == SnakeDirectionEnum.LEFT:
            new_index = head.index - 1
        elif self.current_direction == SnakeDirectionEnum.RIGHT:
            new_index = head.index + 1
        elif self.current_direction == SnakeDirectionEnum.UP:
            new_index = head.index - grid_cols
        elif self.current_direction == SnakeDirectionEnum.DOWN:
            new_index = head.index + grid_cols
    
        new_head = grid_cells[new_index]
    
        # Collision detection
        if new_head in self.cells or new_head in boundary_cells:
            self.collided = True
            return
    
        # Food check
        if new_head == food.cell:
            self.cells.append(new_head)
            self.food_eaten = True
        else:
            self.cells.pop(0)
            self.cells.append(new_head)
    
        self.last_snake_update_time = current_time

    def draw(self):
        for cell in self.cells:
            cell.draw(self.surface, self.color)