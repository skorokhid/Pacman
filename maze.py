import pygame
from constants import (
    BLUE,
    CELL_SIZE,
    GRID_HEIGHT,
    GRID_WIDTH,
    ORANGE,
    WALL,
    PELLET,
    POWER_PELLET,
    YELLOW
)


class Maze:
    def __init__(self):
        self.grid = [
            [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
            [WALL, PELLET, PELLET, PELLET, POWER_PELLET, PELLET, PELLET, WALL, PELLET, PELLET, POWER_PELLET, PELLET, PELLET, PELLET, WALL],
            [WALL, PELLET, WALL, WALL, PELLET, WALL, PELLET, WALL, PELLET, WALL, PELLET, WALL, WALL, PELLET, WALL],
            [WALL, POWER_PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, POWER_PELLET, WALL],
            [WALL, PELLET, WALL, WALL, POWER_PELLET, WALL, WALL, WALL, WALL, WALL, POWER_PELLET, WALL, WALL, PELLET, WALL],
            [WALL, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, WALL, POWER_PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, WALL],
            [WALL, WALL, WALL, WALL, PELLET, WALL, WALL, WALL, WALL, WALL, PELLET, WALL, WALL, WALL, WALL],
            [WALL, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, WALL, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, WALL],
            [WALL, PELLET, WALL, WALL, PELLET, WALL, PELLET, WALL, PELLET, WALL, PELLET, WALL, WALL, PELLET, WALL],
            [WALL, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, WALL],
            [WALL, PELLET, WALL, WALL, PELLET, WALL, WALL, WALL, WALL, WALL, PELLET, WALL, WALL, PELLET, WALL],
            [WALL, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, WALL, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, WALL],
            [WALL, PELLET, WALL, WALL, PELLET, WALL, PELLET, WALL, PELLET, WALL, PELLET, WALL, WALL, PELLET, WALL],
            [WALL, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, WALL, PELLET, PELLET, PELLET, PELLET, PELLET, PELLET, WALL],
            [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
        ]

    def draw(self, screen):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell_value = self.grid[y][x]
                pos_x = x * CELL_SIZE
                pos_y = y * CELL_SIZE + 50  # Зсув для верхньої панелі

                if cell_value == WALL:
                    pygame.draw.rect(
                        screen,
                        BLUE,
                        (pos_x, pos_y, CELL_SIZE, CELL_SIZE))
                elif cell_value == PELLET:
                    center = (
                        pos_x + CELL_SIZE // 2,
                        pos_y + CELL_SIZE // 2
                    )
                    pygame.draw.circle(screen, YELLOW, center, 3)
                elif cell_value == POWER_PELLET:
                    center = (
                        pos_x + CELL_SIZE // 2,
                        pos_y + CELL_SIZE // 2
                    )
                    pygame.draw.circle(screen, ORANGE, center, 6)
