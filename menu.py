import sys
import pygame
from constants import *

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

        # --- Налаштування ---
        settings = {"Easy": (200, 500, 600), "Medium": (150, 400, 500), "Hard": (100, 300, 400)}
        pacman_move_delay, ghost_move_delay, mouth_anim_delay = settings[self.difficulty]
        BG_COLOR = self.bg_colors[self.bg_color]