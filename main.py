import pygame
from game import Game

pygame.init()

EAT_SOUND = pygame.mixer.Sound("./sounds/collect.wav")
LOSE_SOUND = pygame.mixer.Sound("./sounds/lose.wav")
WIN_SOUND = pygame.mixer.Sound("./sounds/win.wav")

FONT = pygame.font.Font(None, 36)

if __name__ == "__main__":
    game = Game()
    game.run()
