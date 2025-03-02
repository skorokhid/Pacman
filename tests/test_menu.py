# tests/test_menu.py
import pytest
from menu import Menu
from constants import *
import pygame

@pytest.fixture
def menu():
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Мокуємо екран
    return Menu(screen)

def test_menu_initialization(menu):
    assert "Start Game" in menu.options

def test_menu_difficulty_selection(menu):
    # Симулюємо натискання клавіші "вправо" для зміни складності
    menu.selected = 0
    menu.update_option(1)  # Зміна на наступну опцію
    assert menu.difficulty in ["Easy", "Medium", "Hard"]