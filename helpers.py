# helpers.py
import os
import pygame

# Constants
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
    screen.fill((0, 0, 0))  # BLACK
    font = pygame.font.Font(None, 40)
    title_text = font.render("High Scores", True, (255, 255, 255))  # WHITE
    screen.blit(title_text, (600 // 2 - title_text.get_width() // 2, 50))
    scores = load_highscores()
    for i, score in enumerate(scores):
        score_text = font.render(f"{i+1}. {score}", True, (255, 255, 255))  # WHITE
        screen.blit(score_text, (600 // 2 - score_text.get_width() // 2, 100 + i * 40))
    pygame.display.flip()
    pygame.time.delay(3000)

def clear_highscores():
    """Очищає файл з рекордами."""
    if os.path.exists(HIGHSCORES_FILE):
        os.remove(HIGHSCORES_FILE)