import pytest
from pacman import PacMan
from constants import *

@pytest.fixture
def pacman():
    return PacMan()
@pytest.mark.parametrize("direction, expected_x, expected_y", [
    (0, 2, 1),  # Рух праворуч
    (1, 1, 2),  # Рух вниз
    (2, 0, 1),  # Рух ліворуч
    (3, 1, 0),  # Рух вгору
])
def test_pacman_move(pacman, direction, expected_x, expected_y):
    pacman.direction = direction
    pacman.move(grid=[[0, 0, 0], [0, 0, 0], [0, 0, 0]], score=0, game_state="PLAYING")
    assert pacman.x == expected_x
    assert pacman.y == expected_y