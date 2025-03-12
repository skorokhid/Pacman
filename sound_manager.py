from constants import eat_sound, lose_sound, win_sound


class SoundManager:
    """Клас для керування звуками гри."""

    @staticmethod
    def play_eat_sound():
        """Відтворює звук поїдання."""
        if eat_sound:
            eat_sound.play()

    @staticmethod
    def play_lose_sound():
        """Відтворює звук програшу."""
        if lose_sound:
            lose_sound.play()

    @staticmethod
    def play_win_sound():
        """Відтворює звук виграшу."""
        if win_sound:
            win_sound.play()
