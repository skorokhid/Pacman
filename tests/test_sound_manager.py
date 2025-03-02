# tests/test_sound_manager.py
from unittest.mock import patch
from sound_manager import SoundManager


@patch.object(SoundManager, "play_eat_sound")
def test_play_eat_sound(mock_play):
    SoundManager.play_eat_sound()
    mock_play.assert_called_once()