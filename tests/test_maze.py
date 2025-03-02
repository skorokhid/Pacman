# tests/test_maze.py
import pytest
from maze import Maze
from constants import *

@pytest.fixture
def maze():
    return Maze()

def test_maze_initialization(maze):
    # Перевіряємо, чи лабіринт містить стіни (значення 1)
    assert any(1 in row for row in maze.grid)


def test_maze_draw(maze, mocker):
    # Ініціалізуємо PyGame
    pygame.init()
    # Створюємо справжню поверхню
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Мокуємо pygame.draw.rect
    mock_draw = mocker.patch("pygame.draw.rect")
    maze.draw(screen)
    # Перевіряємо, чи викликається pygame.draw.rect
    assert mock_draw.call_count > 0