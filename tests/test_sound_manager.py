# tests/test_sound_manager.py
from unittest.mock import patch
from sound_manager import SoundManager

@patch("sound_manager.eat_sound")
def test_play_eat_sound(mock_sound):
    SoundManager.play_eat_sound()
    if mock_sound:  # Перевіряємо, чи звук не None
        mock_sound.play.assert_called_once()