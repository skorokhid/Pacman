from constants import *

class SoundManager:
    @staticmethod
    def play_eat_sound():
         if eat_sound:
            eat_sound.play()

    @staticmethod
    def play_lose_sound():
         if lose_sound:
            lose_sound.play()

    @staticmethod
    def play_win_sound():
         if win_sound:
            win_sound.play()