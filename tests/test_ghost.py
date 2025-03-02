import pytest
from ghost import Ghost
from constants import *

@pytest.fixture
def ghost():
    return Ghost(1, 1, RED)

def test_ghost_move(ghost):
    ghost.move(grid=[[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    assert ghost.x != 1 or ghost.y != 1  # Привид повинен рухатися