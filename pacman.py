import pygame
import math
from constants import BLACK, CELL_SIZE, PELLET, POWER_PELLET, WALL, YELLOW
from game_state import GameState
from sound_manager import SoundManager


class PacMan:
    """Клас, що представляє Пакмана."""

    def __init__(self):
        """Ініціалізація Пакмана."""
        self.x = 1
        self.y = 1
        self.direction = 3
        self.mouth_open = False

    def move(self, grid, score, game_state):
        """Рух Пакмана по карті."""
        dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][self.direction]
        new_x, new_y = self.x + dx, self.y + dy

        if grid[new_y][new_x] != WALL:
            self.x, self.y = new_x, new_y

            if grid[new_y][new_x] == PELLET:
                grid[new_y][new_x] = 2
                score += 10
                SoundManager.play_eat_sound()
            elif grid[new_y][new_x] == POWER_PELLET:
                grid[new_y][new_x] = 2
                score += 50
                SoundManager.play_eat_sound()

            if all(cell not in {0, 4} for row in grid for cell in row):
                game_state = GameState.GAME_WIN
                SoundManager.play_win_sound()

        return score, game_state

    def draw(self, screen):
        """Малює Пакмана на екрані."""
        x = self.x * CELL_SIZE + CELL_SIZE // 2
        y = self.y * CELL_SIZE + CELL_SIZE // 2 + 50
        mouth_opening = 45 if self.mouth_open else 0
        pygame.draw.circle(screen, YELLOW, (x, y), CELL_SIZE // 2)

        angles = {
            0: (360 - mouth_opening / 2, mouth_opening / 2),  # Right
            3: (90 - mouth_opening / 2, 90 + mouth_opening / 2),  # Down
            2: (180 - mouth_opening / 2, 180 + mouth_opening / 2),  # Left
            1: (270 - mouth_opening / 2, 270 + mouth_opening / 2),  # Up
        }
        start_angle, end_angle = angles.get(self.direction, (0, 0))

        pygame.draw.arc(
            screen, BLACK,
            (x - CELL_SIZE // 2, y - CELL_SIZE // 2, CELL_SIZE, CELL_SIZE),
            math.radians(start_angle), math.radians(end_angle), CELL_SIZE // 2
        )

        for angle in (start_angle, end_angle):
            mouth_line_end_x = x + math.cos(math.radians(angle)) * CELL_SIZE // 2
            mouth_line_end_y = y - math.sin(math.radians(angle)) * CELL_SIZE // 2
            pygame.draw.line(screen, BLACK, (x, y), (mouth_line_end_x, mouth_line_end_y), 2)
