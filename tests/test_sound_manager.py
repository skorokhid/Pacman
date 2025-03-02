# tests/test_sound_manager.py
from unittest.mock import patch
from sound_manager import SoundManager


@patch("pygame.mixer.Sound")  # Патчимо pygame.mixer.Sound, щоб не завантажувати звук
@patch.object(SoundManager, "play_eat_sound")
def test_play_eat_sound(mock_play, mock_sound):
    # Під час тесту виклик play_eat_sound не буде викликати реальний pygame.mixer.Sound
    mock_sound.return_value = mock_play  # Ми говоримо, що повертається mock_play, коли викликається Sound
    SoundManager.play_eat_sound()
    mock_play.assert_called_once()
