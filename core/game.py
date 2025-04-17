# /*===================================
#     Stock Imports
# ====================================*/

import pygame
import sys

# /*===================================
#     Main
# ====================================*/

from core.grid import Grid
from core.snake import Snake
from core.food import Food
from models.direction_enum import SnakeDirectionEnum

# milliseconds
GAME_EVENT_LOOP_SPEED = 16  # ~60 fps

class Game:
    def __init__(self, title, screen_width=800, screen_height=600):
        pygame.init()
        pygame.display.set_caption(title)

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.surface = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.font_small = pygame.font.SysFont("arial", 36)
        self.font_large = pygame.font.SysFont("arial", 72)

        self.running = True

        self.surface_color = (0, 0, 0)

        self.directions_queue = []

        self.score = 0
        self.score_color = (255, 255, 255)

        self.grid = Grid(
            self.surface,
            padding={"left": 50, "top": 50, "right": 50, "bottom": 50},
            background_color=(50, 50, 50)  # grey
        )

        self.snake = Snake(self.surface, speed=150)

        # define snake cells
        # grab 5 (any num < grid.width/height) cells that are in center of grid and horizontally aligned
        # NOTE: (can just do: self.snake.spawn([3,4,5,6,7]) for example.)
        cells = []
        row_index = self.grid.rows // 2
        col_start = (self.grid.cols // 2) - (self.snake.size // 2)
        for j in range(col_start, col_start + self.snake.size):
            cells.append(self.grid.cells[row_index * self.grid.cols + j])
        self.snake.spawn(cells)

        # print(f"Snake Cells: {', '.join([str(cell.index) for cell in self.snake.cells])}")

        self.food = Food(self.surface)
        self.food.spawn(self.grid.cells, self.grid.boundary_cells, self.snake.cells)
    
    def run(self):
        # event loop
        while self.running:
            self._handle_events()
            self._render()
            
            self.snake.move(
                self.directions_queue,
                self.grid.cells,
                self.grid.cols,
                self.grid.boundary_cells,
                self.food,
                current_time=pygame.time.get_ticks()
            )

            if self.snake.food_eaten:
                self.score += 10
                self.food.spawn(self.grid.cells, self.grid.boundary_cells, self.snake.cells)
                self.snake.food_eaten = False
            
            # game over check
            if self.snake.collided:
                self._game_over()
                
            self._update()
            self._delay()
    
    def _handle_events(self):
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Close button clicked.")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.directions_queue.append(SnakeDirectionEnum.LEFT)
                elif event.key == pygame.K_UP:
                    self.directions_queue.append(SnakeDirectionEnum.UP)
                elif event.key == pygame.K_RIGHT:
                    self.directions_queue.append(SnakeDirectionEnum.RIGHT)
                elif event.key == pygame.K_DOWN:
                    self.directions_queue.append(SnakeDirectionEnum.DOWN)

    def _render(self):
        # window bg
        self.surface.fill(self.surface_color)

        # score
        self.surface.blit(
            source=self.font_small.render("Score: " + str(self.score), True, self.score_color), 
            dest=(10, 10)
        )

        # grid
        self.grid.draw_background()
        self.grid.draw_lines()
        self.grid.draw_boundary()

        # snake
        self.snake.draw()
        
        # food
        self.food.draw()
    
    def _game_over(self):
        # Fill background
        background_color = (0, 0, 0)
        self.surface.fill(background_color)

        # Render text
        text_game_over = self.font_large.render("Game Over", True, (255, 0, 0))
        text_score = self.font_small.render("Score: " + str(self.score), True, (255, 255, 255))
        text_prompt = self.font_small.render("Press any key to exit", True, (200, 200, 200))

        # Get rectangles to center text
        rect_game_over = text_game_over.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2 - 60))
        rect_score = text_score.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2))
        rect_prompt = text_prompt.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2 + 60))

        # Draw text
        self.surface.blit(text_game_over, rect_game_over)
        self.surface.blit(text_score, rect_score)
        self.surface.blit(text_prompt, rect_prompt)
        pygame.display.flip()

        # Wait for key press or quit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
        
        pygame.quit()
        sys.exit()

    def _update(self):
        pygame.display.update()
    
    def _delay(self):
        pygame.time.delay(GAME_EVENT_LOOP_SPEED)
