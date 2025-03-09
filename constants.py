# constants.py
import pygame
import os
 
pygame.init()

if pygame.mixer.get_init() is None:
    try:
        pygame.mixer.init()
    except pygame.error:
        print("Sound system initialization failed. Sounds disabled.")
        SOUND_ENABLED = False
    else:
        SOUND_ENABLED = True
else:
    SOUND_ENABLED = True
    
if SOUND_ENABLED:
    eat_sound = pygame.mixer.Sound("./sounds/collect.wav")
    lose_sound = pygame.mixer.Sound("./sounds/lose.wav")
    win_sound = pygame.mixer.Sound("./sounds/win.wav")
else:
    eat_sound = None
    lose_sound = None
    win_sound = None
# Initialize font
font = pygame.font.Font(None, 36)

# Constants
WALL = 1
PELLET = 0
POWER_PELLET = 4
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

# Delays for game mechanics
pacman_move_delay = 150  # Default value
ghost_move_delay = 400   # Default value
mouth_anim_delay = 500   # Default value