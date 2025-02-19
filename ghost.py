import pygame
import random
from constants import *

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self, grid):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x, new_y = self.x + dx, self.y + dy
            # Перевірка на межі лабіринту
            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                if grid[new_y][new_x] != 1:  # Перевірка на стіну
                    self.x, self.y = new_x, new_y
                    break

    def draw(self, screen):
        x = self.x * CELL_SIZE + CELL_SIZE // 2
        y = self.y * CELL_SIZE + CELL_SIZE // 2 + 50
        pygame.draw.circle(screen, self.color, (x, y), CELL_SIZE // 2)