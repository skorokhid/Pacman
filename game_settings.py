import argparse
from constants import PINK, GRAY, BLACK  # явний імпорт констант


class GameSettings:
    def __init__(self, test_mode=False):
        self.difficulty = 'easy'  # узгоджуємо з дефолтним значенням argparse
        self.bg_color = 'black'
        self.pacman_move_delay = 150
        self.ghost_move_delay = 400
        self.mouth_anim_delay = 500
        if not test_mode:
            self.parse_args()
            self.set_delays()  # викликаємо налаштування затримок

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description="Pac-Man Game Settings"
        )
        parser.add_argument(
            '--difficulty',
            type=str,
            choices=['easy', 'medium', 'hard'],
            default='easy',
            help="Set the game difficulty"
        )
        parser.add_argument(
            '--bg_color',
            type=str,
            choices=['black', 'pink', 'gray'],
            default='black',
            help="Set the background color"
        )
        args = parser.parse_args()
        self.difficulty = args.difficulty
        self.bg_color = args.bg_color

    def set_delays(self):
        """Встановлює затримки на основі складності"""
        if self.difficulty == 'easy':
            self.pacman_move_delay = 200
            self.ghost_move_delay = 500
            self.mouth_anim_delay = 600
        elif self.difficulty == 'medium':
            self.pacman_move_delay = 150
            self.ghost_move_delay = 400
            self.mouth_anim_delay = 500
        else:  # 'hard'
            self.pacman_move_delay = 100
            self.ghost_move_delay = 300
            self.mouth_anim_delay = 400

    def get_bg_color(self):
        """Повертає колір фону на основі налаштувань."""
        if self.bg_color == 'pink':
            return PINK
        if self.bg_color == 'gray':
            return GRAY
        return BLACK  # дефолтне значення (чорний)
