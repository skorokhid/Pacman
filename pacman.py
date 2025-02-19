import pygame
import math
from constants import *
from game_state import GameState
from sound_manager import SoundManager

class PacMan:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.direction = 3  # 0: right, 1: down, 2: left, 3: up
        self.mouth_open = False

    def move(self, grid, score, game_state):
        dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][self.direction]
        new_x, new_y = self.x + dx, self.y + dy
        if grid[new_y][new_x] != 1:
            self.x, self.y = new_x, new_y
            if grid[new_y][new_x] == 0:
                grid[new_y][new_x] = 2  
                score += 10
                SoundManager.play_eat_sound()
            elif grid[new_y][new_x] == 4:  # Заряджений бонус
                grid[new_y][new_x] = 2  
                score += 50
                SoundManager.play_eat_sound()
            if all(cell != 0 and cell != 4 for row in grid for cell in row):  # Перевірка на перемогу
                game_state = GameState.GAME_WIN
                SoundManager.play_win_sound()
        return score, game_state

    def draw(self, screen):
        x = self.x * CELL_SIZE + CELL_SIZE // 2
        y = self.y * CELL_SIZE + CELL_SIZE // 2 + 50
        mouth_opening = 45 if self.mouth_open else 0
        pygame.draw.circle(screen, YELLOW, (x, y), CELL_SIZE // 2)
        if self.direction == 0:  # Right
            start_angle = 360 - mouth_opening / 2
            end_angle = mouth_opening / 2
        elif self.direction == 3:  # Down
            start_angle = 90 - mouth_opening / 2
            end_angle = 90 + mouth_opening / 2
        elif self.direction == 2:  # Left
            start_angle = 180 - mouth_opening / 2
            end_angle = 180 + mouth_opening / 2
        else:  # Ups
            start_angle = 270 - mouth_opening / 2
            end_angle = 270 + mouth_opening / 2
        pygame.draw.arc(screen, BLACK, (x - CELL_SIZE // 2, y - CELL_SIZE // 2, CELL_SIZE, CELL_SIZE), math.radians(start_angle), math.radians(end_angle), CELL_SIZE // 2)
        mouth_line_end_x = x + math.cos(math.radians(start_angle)) * CELL_SIZE // 2
        mouth_line_end_y = y - math.sin(math.radians(start_angle)) * CELL_SIZE // 2
        pygame.draw.line(screen, BLACK, (x, y), (mouth_line_end_x, mouth_line_end_y), 2)
        mouth_line_end_x = x + math.cos(math.radians(end_angle)) * CELL_SIZE // 2
        mouth_line_end_y = y - math.sin(math.radians(end_angle)) * CELL_SIZE // 2
        pygame.draw.line(screen, BLACK, (x, y), (mouth_line_end_x, mouth_line_end_y), 2)