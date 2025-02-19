import pygame
import random
import math
import argparse
import os


# Ініціалізація pygame
pygame.init()

# Initialize sound variables
eat_sound = pygame.mixer.Sound("./sounds/collect.wav")
lose_sound = pygame.mixer.Sound("./sounds/lose.wav")
win_sound = pygame.mixer.Sound("./sounds/win.wav")

# Initialize font
font = pygame.font.Font(None, 36)

# Constants
CELL_SIZE = 40
GRID_WIDTH = 15
GRID_HEIGHT = 15
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GRAY = (80, 80, 80)
VIOLET = (151, 89, 154)

HIGHSCORES_FILE = "highscores.txt"

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
            menu_text = font.render(text, True, color)
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

class GameSettings:
    def __init__(self):
        self.difficulty = 'medium'
        self.bg_color = 'black'
        self.parse_args()

    def parse_args(self):
        parser = argparse.ArgumentParser(description="Pac-Man Game Settings")
        parser.add_argument('--difficulty', type=str, choices=['easy', 'medium', 'hard'], default='easy', help="Set the game difficulty")
        parser.add_argument('--bg_color', type=str, choices=['black', 'pink', 'gray'], default='black', help="Set the background color")
        args = parser.parse_args()
        self.difficulty = args.difficulty
        self.bg_color = args.bg_color

        # Set delays based on difficulty
        global pacman_move_delay, ghost_move_delay, mouth_anim_delay
        if self.difficulty == 'easy':      
            pacman_move_delay = 200
            ghost_move_delay = 500
            mouth_anim_delay = 600
        elif self.difficulty == 'medium':
            pacman_move_delay = 150
            ghost_move_delay = 400
            mouth_anim_delay = 500
        else:  # 'hard' 
            pacman_move_delay = 100
            ghost_move_delay = 300
            mouth_anim_delay = 400

        # Set background color
        global BG_COLOR
        if self.bg_color == 'pink':
            BG_COLOR = PINK
        elif self.bg_color == 'gray':
            BG_COLOR = GRAY
        else:  # 'default(black)'
            BG_COLOR = BLACK

class PacMan:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.direction = 3  # 0: right, 1: down, 2: left, 3: up
        self.mouth_open = False

    def move(self, grid, score, game_state):
        dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][self.direction]
        new_x, new_y = self.x + dx, self.y + dy
        if grid[new_y][new_x] != 1:
            self.x, self.y = new_x, new_y
            if grid[new_y][new_x] == 0:
                grid[new_y][new_x] = 2  # Mark as eaten
                score += 10
                SoundManager.play_eat_sound()
                if all(cell != 0 for row in grid for cell in row):
                    game_state = GameState.GAME_WIN
                    SoundManager.play_win_sound()
        return score, game_state

    def draw(self, screen):
        x = self.x * CELL_SIZE + CELL_SIZE // 2
        y = self.y * CELL_SIZE + CELL_SIZE // 2 + 50
        mouth_opening = 45 if self.mouth_open else 0
        pygame.draw.circle(screen, YELLOW, (x, y), CELL_SIZE // 2)
        if self.direction == 0:  # Right
            start_angle = 360 - mouth_opening / 2
            end_angle = mouth_opening / 2
        elif self.direction == 3:  # Down
            start_angle = 90 - mouth_opening / 2
            end_angle = 90 + mouth_opening / 2
        elif self.direction == 2:  # Left
            start_angle = 180 - mouth_opening / 2
            end_angle = 180 + mouth_opening / 2
        else:  # Ups
            start_angle = 270 - mouth_opening / 2
            end_angle = 270 + mouth_opening / 2
        pygame.draw.arc(screen, BLACK, (x - CELL_SIZE // 2, y - CELL_SIZE // 2, CELL_SIZE, CELL_SIZE), math.radians(start_angle), math.radians(end_angle), CELL_SIZE // 2)
        mouth_line_end_x = x + math.cos(math.radians(start_angle)) * CELL_SIZE // 2
        mouth_line_end_y = y - math.sin(math.radians(start_angle)) * CELL_SIZE // 2
        pygame.draw.line(screen, BLACK, (x, y), (mouth_line_end_x, mouth_line_end_y), 2)
        mouth_line_end_x = x + math.cos(math.radians(end_angle)) * CELL_SIZE // 2
        mouth_line_end_y = y - math.sin(math.radians(end_angle)) * CELL_SIZE // 2
        pygame.draw.line(screen, BLACK, (x, y), (mouth_line_end_x, mouth_line_end_y), 2)

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self, grid):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and grid[new_y][new_x] != 1:
                self.x, self.y = new_x, new_y
                break

    def draw(self, screen):
        x = self.x * CELL_SIZE + CELL_SIZE // 2
        y = self.y * CELL_SIZE + CELL_SIZE // 2 + 50
        pygame.draw.circle(screen, self.color, (x, y), CELL_SIZE // 2)

class Maze:
    def __init__(self):
        self.grid = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
            [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,0,1,1,1,1,1,0,1,1,0,1],
            [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
            [1,1,1,1,0,1,0,1,0,1,0,1,1,1,1],
            [1,1,1,1,0,1,0,0,0,1,0,1,1,1,1],
            [1,1,1,1,0,1,0,1,0,1,0,1,1,1,1],
            [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
            [1,0,1,1,0,1,1,1,1,1,0,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
            [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]

    def draw(self, screen):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] == 1:
                    pygame.draw.rect(screen, BLUE, (x*CELL_SIZE, y*CELL_SIZE+50, CELL_SIZE, CELL_SIZE))
                elif self.grid[y][x] == 0:
                    pygame.draw.circle(screen, YELLOW, (x*CELL_SIZE+CELL_SIZE//2, y*CELL_SIZE+CELL_SIZE//2+50), 3)

class SoundManager:
    @staticmethod
    def play_eat_sound():
        eat_sound.play()

    @staticmethod
    def play_lose_sound():
        lose_sound.play()

    @staticmethod
    def play_win_sound():
        win_sound.play()

class ScoreManager:
    def __init__(self):
        self.score = 0

    def draw(self, screen):
        score_text = font.render(f"score:{self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

class GameState:
    PLAYING = 0
    GAME_OVER = 1
    GAME_WIN = 2

class Game:
    def __init__(self):
        self.settings = GameSettings()
        self.pacman = PacMan()
        self.ghosts = [Ghost(1, 13, RED), Ghost(13, 1, VIOLET), Ghost(13, 13, CYAN), Ghost(11, 11, ORANGE)]
        self.maze = Maze()
        self.score_manager = ScoreManager()
        self.game_state = GameState.PLAYING
        self.last_pacman_move_time = 0
        self.last_ghost_move_time = 0
        self.last_mouth_anim_time = 0

    def reset_game(self):
        self.pacman = PacMan()
        self.ghosts = [Ghost(1, 13, RED), Ghost(13, 1, VIOLET), Ghost(13, 13, CYAN), Ghost(11, 11, ORANGE)]
        self.maze = Maze()
        self.score_manager = ScoreManager()
        self.game_state = GameState.PLAYING

    def draw_game_over(self, screen):
        screen.fill(BLACK)
        game_over_font = pygame.font.Font(None, 64)
        score_font = pygame.font.Font(None, 48)
        restart_font = pygame.font.Font(None, 36)
        game_over_text = game_over_font.render("GAME OVER", True, RED)
        score_text = score_font.render(f"Score: {self.score_manager.score}", True, WHITE)

        restart_text = restart_font.render("Press SPACE to restart or ESC for menu", True, YELLOW)
        restart_text = restart_font.render("Press SPACE to restart", True, YELLOW)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 2 * SCREEN_HEIGHT // 3))

    def draw_game_win(self, screen):
        screen.fill(BLACK)
        win_font = pygame.font.Font(None, 64)
        score_font = pygame.font.Font(None, 48)
        restart_font = pygame.font.Font(None, 36)
        win_text = win_font.render("YOU WIN!", True, YELLOW)
        score_text = score_font.render(f"Score: {self.score_manager.score}", True, WHITE)
        restart_text = restart_font.render("Press SPACE to restart or ESC for menu", True, CYAN)
        restart_text = restart_font.render("Press SPACE to restart", True, CYAN)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 2 * SCREEN_HEIGHT // 3))

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        clock = pygame.time.Clock()
        running = True

        # Show menu before starting the game
        menu = Menu(screen)
        menu.run()
        
        while running:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.game_state == GameState.PLAYING:
                        if event.key == pygame.K_UP:
                            self.pacman.direction = 3
                        elif event.key == pygame.K_DOWN:
                            self.pacman.direction = 1
                        elif event.key == pygame.K_LEFT:
                            self.pacman.direction = 2
                        elif event.key == pygame.K_RIGHT:
                            self.pacman.direction = 0
                    elif self.game_state in [GameState.GAME_OVER, GameState.GAME_WIN]:
                        if event.key == pygame.K_SPACE:
                            self.reset_game()

                        elif event.key == pygame.K_ESCAPE:
                            menu.run()  # Повернутися до меню


            if self.game_state == GameState.PLAYING:
                if current_time - self.last_pacman_move_time > pacman_move_delay:
                    self.score_manager.score, self.game_state = self.pacman.move(self.maze.grid, self.score_manager.score, self.game_state)
                    self.last_pacman_move_time = current_time
                if current_time - self.last_ghost_move_time > ghost_move_delay:
                    for ghost in self.ghosts:
                        ghost.move(self.maze.grid)
                    self.last_ghost_move_time = current_time
                if current_time - self.last_mouth_anim_time > mouth_anim_delay:
                    self.pacman.mouth_open = not self.pacman.mouth_open
                    self.last_mouth_anim_time = current_time

                screen.fill(BG_COLOR)
                self.maze.draw(screen)
                self.pacman.draw(screen)
                for ghost in self.ghosts:
                    ghost.draw(screen)
                self.score_manager.draw(screen)

                for ghost in self.ghosts:
                    if self.pacman.x == ghost.x and self.pacman.y == ghost.y:
                        self.game_state = GameState.GAME_OVER
                        SoundManager.play_lose_sound()

            elif self.game_state == GameState.GAME_OVER:
                self.draw_game_over(screen)
            elif self.game_state == GameState.GAME_WIN:
                self.draw_game_win(screen)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

# Initialize game
game = Game()
game.run()