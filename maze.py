import pygame
from constants import BLUE, CELL_SIZE, GRID_HEIGHT, GRID_WIDTH, ORANGE, WALL, PELLET, POWER_PELLET, YELLOW

class Maze:
    def __init__(self):
        self.grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 4, 0, 0, 1, 0, 0, 4, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
            [1, 0, 1, 1, 4, 1, 1, 1, 1, 1, 4, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 4, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def draw(self, screen):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] == WALL:
                    pygame.draw.rect(screen, BLUE, (x*CELL_SIZE, y*CELL_SIZE+50, CELL_SIZE, CELL_SIZE))
                elif self.grid[y][x] == PELLET:
                    pygame.draw.circle(screen, YELLOW, (x*CELL_SIZE+CELL_SIZE//2, y*CELL_SIZE+CELL_SIZE//2+50), 3)
                elif self.grid[y][x] == POWER_PELLET:  
                    pygame.draw.circle(screen, ORANGE, (x*CELL_SIZE+CELL_SIZE//2, y*CELL_SIZE+CELL_SIZE//2+50), 6)