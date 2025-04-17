# /*===================================
#     Stock Imports
# ====================================*/

import pygame

# /*===================================
#     Main
# ====================================*/

from core.cell import Cell

class Grid:
    def __init__(self,  
        surface,
        rows=20, 
        cols=20, 
        padding={"left": 0, "top": 0, "right": 0, "bottom": 0},
        background_color=(0, 0, 0),
        line_color=(125, 125, 125),
        boundary_color=(128, 0, 32)
    ):
        self.surface = surface
        self.rows = rows
        self.cols = cols
        self.padding = padding
        self.background_color = background_color
        self.line_color = line_color
        self.boundary_color = boundary_color

        # The order of the following attributes is important!
        self.width, self.height = self._set_grid_size()

        self.cell_width = self.width // self.rows
        self.cell_height = self.height // self.cols

        self.cells = self._set_cells()
        self.boundary_cells = self._set_boundary_cells()

    def _set_grid_size(self):
        width = self.surface.get_width() - self.padding["left"] - self.padding["right"]
        height = self.surface.get_height() - self.padding["top"] - self.padding["bottom"]

        # print(f"Grid dimensions: {self.width}x{self.height}")

        return width, height

    def _set_cells(self):
        cells = []
        for i in range(self.rows * self.cols):
            col = i % self.cols
            row = i // self.cols
            x = self.padding["left"] + col * self.cell_width
            y = self.padding["top"] + row * self.cell_height
            cell = Cell(
                index=i,
                x=x,
                y=y,
                width=self.cell_width,
                height=self.cell_height
            )
            cells.append(cell)
        
        # visualize grid
        # for row in range(self.rows):
        #     print(" ".join(f"{self.cells[row * self.cols + col].index:3}" for col in range(self.cols)))

        return cells

    def _set_boundary_cells(self):
        if len(self.cells) == 0:
            return []

        cells = []
        for row in range(self.rows):
            for col in range(self.cols):
                is_top = row == 0
                is_bottom = row == self.rows - 1
                is_left = col == 0
                is_right = col == self.cols - 1
        
                if is_top or is_bottom or is_left or is_right:
                    index = row * self.cols + col
                    cells.append(self.cells[index])

        # print(f"Edge Cells: {', '.join([str(cell.index) for cell in self.boundary_cells])}")

        return cells

    def draw_background(self):
        pygame.draw.rect(
            self.surface,
            self.background_color,
            (
                self.padding["left"],
                self.padding["top"],
                self.width,
                self.height
            )
        )
    
    def draw_lines(self):
        # Draw vertical grid lines (columns)
        for x in range(self.cols + 1):
            x_pos = self.padding["left"] + x * self.cell_width
            pygame.draw.line(
                self.surface,
                self.line_color,
                start_pos=(x_pos, self.padding["top"]),
                end_pos=(x_pos, self.height + self.padding["top"])
            )
        
        # Draw horizontal grid lines (rows)
        for y in range(self.rows + 1):
            y_pos = self.padding["top"] + y * self.cell_height
            pygame.draw.line(
                self.surface,
                self.line_color,
                start_pos=(self.padding["left"], y_pos),
                end_pos=(self.width + self.padding["left"], y_pos)
            )
    
    def draw_boundary(self):
        for cell in self.boundary_cells:
            pygame.draw.rect(self.surface, self.boundary_color, cell.rect)