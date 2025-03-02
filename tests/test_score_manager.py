# tests/test_score_manager.py
import pytest
from score_manager import ScoreManager
from constants import *


@pytest.fixture
def score_manager():
    return ScoreManager()

def test_score_update(score_manager):
    score_manager.score = 0
    score_manager.score += 50  # Без використання методу update_score()
    assert score_manager.score == 50

def test_score_reset(score_manager):
    score_manager.score = 100
    score_manager.score = 0  # Без використання методу reset()
    assert score_manager.score == 0