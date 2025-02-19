# game_settings.py
import argparse
from constants import *

class GameSettings:
    def __init__(self):
        self.difficulty = 'medium'
        self.bg_color = 'black'
        self.parse_args()

    def parse_args(self):
        parser = argparse.ArgumentParser(description="Pac-Man Game Settings")
        parser.add_argument('--difficulty', type=str, choices=['easy', 'medium', 'hard'], default='easy', help="Set the game difficulty")
        parser.add_argument('--bg_color', type=str, choices=['black', 'pink', 'gray'], default='black', help="Set the background color")
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
        global BG_COLOR
        if self.bg_color == 'pink':
            BG_COLOR = PINK
        elif self.bg_color == 'gray':
            BG_COLOR = GRAY
        else:  # 'default(black)'
            BG_COLOR = BLACK