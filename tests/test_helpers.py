# tests/test_helpers.py
import pytest
from helpers import save_highscore, load_highscores, clear_highscores
import os


def test_save_and_load_highscores(tmp_path, monkeypatch):
    # Тимчасово змінюємо шлях до файлу рекордів
    test_file = tmp_path / "test_highscores.txt"
    monkeypatch.setattr("helpers.HIGHSCORES_FILE", test_file)
    
    save_highscore(100)
    assert load_highscores() == [100]

def test_clear_highscores(tmp_path, monkeypatch):
    test_file = tmp_path / "test_highscores.txt"
    monkeypatch.setattr("helpers.HIGHSCORES_FILE", test_file)
    
    save_highscore(100)
    clear_highscores()
    assert not test_file.exists()