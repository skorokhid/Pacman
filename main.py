import argparse
import pygame
import math
import random
class GameSettings:
    def init(self):
        self.difficulty = 'medium'
        self.bg_color = 'black'
        self.parse_args()

    def parse_args(self):
        parser = argparse.ArgumentParser(description="Pac-Man Game Settings")
        parser.add_argument('--difficulty', type=str, choices=['easy', 'medium', 'hard'], default='hard', help="Set the game difficulty")
        parser.add_argument('--bg_color', type=str, choices=['black', 'pink', 'gray'], default='pink', help="Set the background color")
        args = parser.parse_args()
        self.difficulty = args.difficulty
        self.bg_color = args.bg_color

        # Set delays based on difficulty
        global pacman_move_delay, ghost_move_delay, mouth_anim_delay
        if self.difficulty == 'easy':
            pacman_move_delay = 200
            ghost_move_delay = 500
            mouth_anim_delay = 600
        elif self.difficulty == 'medium':
            pacman_move_delay = 150
            ghost_move_delay = 400
            mouth_anim_delay = 500
        else:  # 'hard' 
            pacman_move_delay = 100
            ghost_move_delay = 300
            mouth_anim_delay = 400

        # Set background color
        global BG_COLOR, PINK, GRAY, BLACK
        PINK = (255, 192, 203)
        GRAY = (80, 80, 80)
        BLACK = (0, 0, 0)

        if self.bg_color == 'pink':
            BG_COLOR = PINK
        elif self.bg_color == 'gray':
            BG_COLOR = GRAY
        else:
            BG_COLOR = BLACK


pygame.init()

# Load sounds
eat_sound = pygame.mixer.Sound("./sounds/collect.wav")
lose_sound = pygame.mixer.Sound("./sounds/lose.wav")
win_sound = pygame.mixer.Sound("./sounds/win.wav")

class SoundManager:
    @staticmethod
    def play_eat_sound():
        eat_sound.play()

    @staticmethod
    def play_lose_sound():
        lose_sound.play()

    @staticmethod
    def play_win_sound():
        win_sound.play()
        


CELL_SIZE = 40
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
VIOLET = (151, 89, 154)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

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
                grid[new_y][new_x] = 2  # Mark as eaten
                score += 10
        return score, game_state

    def draw(self, screen):
        x = self.x * CELL_SIZE + CELL_SIZE // 2
        y = self.y * CELL_SIZE + CELL_SIZE // 2 + 50
        pygame.draw.circle(screen, YELLOW, (x, y), CELL_SIZE // 2)

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
            if grid[new_y][new_x] != 1:
                self.x, self.y = new_x, new_y
                break

    def draw(self, screen):
        x = self.x * CELL_SIZE + CELL_SIZE // 2
        y = self.y * CELL_SIZE + CELL_SIZE // 2 + 50
        pygame.draw.circle(screen, self.color, (x, y), CELL_SIZE // 2)
