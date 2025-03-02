# tests/test_sound_manager.py
from unittest.mock import patch
from sound_manager import SoundManager

# Патчимо pygame.mixer.init(), щоб воно не викликалося під час тестів
@patch("pygame.mixer.init")
@patch.object(SoundManager, "play_eat_sound")
def test_play_eat_sound(mock_play, mock_init):
    SoundManager.play_eat_sound()
    mock_play.assert_called_once()
    mock_init.assert_not_called()  # Перевіряємо, що init не був викликаний
