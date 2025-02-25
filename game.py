import pygame
import sys
from helpers import clear_highscores, draw_highscores, save_highscore
from menu import Menu
from game_settings import GameSettings
from pacman import PacMan
from ghost import Ghost
from maze import Maze
from sound_manager import SoundManager
from score_manager import ScoreManager
from game_state import GameState
from constants import *

class Game:
    def __init__(self):
        self.settings = GameSettings()  # Створюємо екземпляр GameSettings
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
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 2 * SCREEN_HEIGHT // 3))

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        clock = pygame.time.Clock()
        running = True

        # Показуємо меню перед початком гри
        menu = Menu(screen)
        settings = menu.run()  # Отримуємо налаштування з меню

        # Застосовуємо налаштування
        global pacman_move_delay, ghost_move_delay, mouth_anim_delay, BG_COLOR
        pacman_move_delay, ghost_move_delay, mouth_anim_delay = settings["delays"]
        BG_COLOR = settings["bg_color"]

        while running:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    clear_highscores()
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
                            settings = menu.run()  # Повертаємося до меню
                            pacman_move_delay, ghost_move_delay, mouth_anim_delay = settings["delays"]
                            BG_COLOR = settings["bg_color"]

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

                # Використовуємо BG_COLOR для фону
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
                save_highscore(self.score_manager.score)
                self.draw_game_over(screen)
                pygame.display.flip()
                pygame.time.delay(2000)
                draw_highscores(screen)

            elif self.game_state == GameState.GAME_WIN:
                save_highscore(self.score_manager.score)
                self.draw_game_win(screen)
                pygame.display.flip()
                pygame.time.delay(2000)
                draw_highscores(screen)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()