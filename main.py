
import pygame
from game import Game
from helpers import load_highscores, save_highscore, draw_highscores, clear_highscores

pygame.init()

# Initialize sound variables
eat_sound = pygame.mixer.Sound("./sounds/collect.wav")
lose_sound = pygame.mixer.Sound("./sounds/lose.wav")
win_sound = pygame.mixer.Sound("./sounds/win.wav")

# Initialize font
font = pygame.font.Font(None, 36)

if __name__ == "__main__":
    game = Game()
    game.run()