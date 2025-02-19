import pygame
import sys
import random
import math
import os

pygame.init()

# --- Константи ---
CELL_SIZE = 40
GRID_WIDTH, GRID_HEIGHT = 15, 15
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 650
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
BLUE, YELLOW, RED = (0, 0, 255), (255, 255, 0), (255, 0, 0)
PINK, CYAN, ORANGE, GRAY = (255, 192, 203), (0, 255, 255), (255, 165, 0), (80, 80, 80)
VIOLET = (151, 89, 154)
FONT = pygame.font.Font(None, 36)
HIGHSCORES_FILE = "highscores.txt"

# --- Глобальні змінні для складності ---
pacman_move_delay, ghost_move_delay, mouth_anim_delay = 150, 400, 500
BG_COLOR = BLACK

# --- Функції для роботи з рекордами ---
def load_highscores():
    if os.path.exists(HIGHSCORES_FILE):
        with open(HIGHSCORES_FILE, "r") as file:
            scores = [int(line.strip()) for line in file.readlines()]
        return sorted(scores, reverse=True)[:5]
    return []

def save_highscore(new_score):
    scores = load_highscores() + [new_score]
    scores = sorted(scores, reverse=True)[:5]
    with open(HIGHSCORES_FILE, "w") as file:
        for score in scores:
            file.write(f"{score}\n")

def draw_highscores(screen):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 40)
    title_text = font.render("High Scores", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
    scores = load_highscores()
    for i, score in enumerate(scores):
        score_text = font.render(f"{i+1}. {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 100 + i * 40))
    pygame.display.flip()
    pygame.time.delay(3000)

# --- Клас меню ---
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ["Difficulty: Medium", "Background: Black", "Start Game"]
        self.difficulties = ["Easy", "Medium", "Hard"]
        self.bg_colors = {"Black": BLACK, "Pink": PINK, "Gray": GRAY}
        self.selected = 0
        self.difficulty = "Medium"
        self.bg_color = "Black"

    def draw(self):
        self.screen.fill(BLACK)
        for i, text in enumerate(self.options):
            color = YELLOW if i == self.selected else WHITE
            menu_text = FONT.render(text, True, color)
            self.screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 200 + i * 50))
        pygame.display.flip()

    def update_option(self, direction):
        if self.selected == 0:
            idx = self.difficulties.index(self.difficulty) + direction
            self.difficulty = self.difficulties[idx % len(self.difficulties)]
            self.options[0] = f"Difficulty: {self.difficulty}"
        elif self.selected == 1:
            bg_list = list(self.bg_colors.keys())
            idx = bg_list.index(self.bg_color) + direction
            self.bg_color = bg_list[idx % len(bg_list)]
            self.options[1] = f"Background: {self.bg_color}"

    def run(self):
        global pacman_move_delay, ghost_move_delay, mouth_anim_delay, BG_COLOR
        running = True
        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        direction = -1 if event.key == pygame.K_LEFT else 1
                        self.update_option(direction)
                    elif event.key == pygame.K_RETURN and self.selected == 2:
                        running = False


        # --- Налаштування складності ---
        settings = {"Easy": (200, 500, 600), "Medium": (150, 400, 500), "Hard": (100, 300, 400)}
        pacman_move_delay, ghost_move_delay, mouth_anim_delay = settings[self.difficulty]
        BG_COLOR = self.bg_colors[self.bg_color]

# --- Класи гри ---
class PacMan:
    def __init__(self):
        self.x, self.y, self.direction = 1, 1, 3
        self.mouth_open = False

    def move(self, grid, score):
        dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][self.direction]
        new_x, new_y = self.x + dx, self.y + dy
        if grid[new_y][new_x] != 1:
            self.x, self.y = new_x, new_y
            if grid[new_y][new_x] in (0, 3):
                score += 50 if grid[new_y][new_x] == 3 else 10
                grid[new_y][new_x] = 2
        return score

class Ghost:
    def __init__(self, x, y, color):
        self.x, self.y, self.color = x, y, color

    def move(self, grid):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid):  # Запобігання виходу за межі
                if grid[new_y][new_x] != 1:
                    self.x, self.y = new_x, new_y
                    break

class Maze:
    def __init__(self):
        self.grid = [
            [1]*15,
            [1,0,0,0,3,0,0,1,0,0,0,3,0,0,1],
            [1,0,1,1,0,1,0,1,0,1,3,1,1,0,1],
            [1,3,0,0,0,0,0,0,0,0,0,0,0,3,1],
            [1,0,1,1,3,1,1,1,1,1,0,1,1,0,1],
            [1,0,0,0,0,0,0,1,3,0,0,0,0,0,1],
            [1]*15,
        ]

# --- Основна гра ---
def run_game():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pac-Man")
    menu = Menu(screen)
    menu.run()
    
    pacman = PacMan()
    ghosts = [Ghost(1, 13, RED), Ghost(13, 1, VIOLET)]
    maze = Maze()
    score, running = 0, True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        score = pacman.move(maze.grid, score)
        for ghost in ghosts:
            ghost.move(maze.grid)
        screen.fill(BG_COLOR)
        
        pygame.display.flip()
        pygame.time.delay(100)

    save_highscore(score)
    draw_highscores(screen)

run_game()
