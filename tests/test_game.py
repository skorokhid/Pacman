# tests/test_game.py
import pytest
from unittest.mock import patch
from game import Game
from game_state import GameState


@pytest.fixture
def game():
    # Мокуємо GameSettings, щоб він не викликав argparse
    with patch("game_settings.GameSettings.parse_args") as mock_parse:
        mock_parse.return_value = None  # Ігноруємо парсинг аргументів
        return Game()

def test_game_initialization(game):
    assert game.game_state == GameState.PLAYING
    assert len(game.ghosts) == 4

def test_game_reset(game):
    game.game_state = GameState.GAME_OVER
    game.reset_game()
    assert game.game_state == GameState.PLAYING