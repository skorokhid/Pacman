import os
import pygame
import sys
from game import Game

pygame.init()

# Initialize sound variables
eat_sound = pygame.mixer.Sound("./sounds/collect.wav")
lose_sound = pygame.mixer.Sound("./sounds/lose.wav")
win_sound = pygame.mixer.Sound("./sounds/win.wav")

# Initialize font
font = pygame.font.Font(None, 36)

# Constants
CELL_SIZE = 40
GRID_WIDTH = 15
GRID_HEIGHT = 15
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GRAY = (80, 80, 80)
VIOLET = (151, 89, 154)

HIGHSCORES_FILE = "highscores.txt"

def load_highscores():
    if os.path.exists(HIGHSCORES_FILE):
        with open(HIGHSCORES_FILE, "r") as file:
            scores = [int(line.strip()) for line in file.readlines()]
        return sorted(scores, reverse=True)[:5]
    return []

def save_highscore(new_score):
    scores = load_highscores()
    scores.append(new_score)
    scores = sorted(scores, reverse=True)[:5]
    with open(HIGHSCORES_FILE, "w") as file:
        for score in scores:
            file.write(f"{score}\n")

def draw_highscores(screen):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 40)
    title_text = font.render("High Scores", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
    scores = load_highscores()
    for i, score in enumerate(scores):
        score_text = font.render(f"{i+1}. {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 100 + i * 40))
    pygame.display.flip()
    pygame.time.delay(3000)

def clear_highscores():
    """Очищає файл з рекордами."""
    if os.path.exists(HIGHSCORES_FILE):
        os.remove(HIGHSCORES_FILE)

if __name__ == "__main__":
    game = Game()
    game.run()