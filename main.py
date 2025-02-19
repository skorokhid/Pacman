import pygame
import random
import sys

# Ініціалізація pygame
pygame.init()

# Константи екрану
WIDTH, HEIGHT = 500, 500
CELL_SIZE = 25
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
FPS = 10

# Кольори
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Фони
BACKGROUND_COLORS = {
    "Black": BLACK,
    "White": WHITE,
    "Green": GREEN,
    "Blue": BLUE
}

# Меню вибору складності та кольору фону
def menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man Menu")
    font = pygame.font.Font(None, 36)
    
    difficulties = ["Easy", "Medium", "Hard"]
    background_names = list(BACKGROUND_COLORS.keys())
    
    selected_difficulty = 1  # За замовчуванням Medium
    selected_background = 0   # За замовчуванням Black
    
    while True:
        screen.fill(WHITE)
        title = font.render("Select Difficulty and Background", True, BLACK)
        screen.blit(title, (50, 50))
        
        for i, diff in enumerate(difficulties):
            color = RED if i == selected_difficulty else BLACK
            text = font.render(diff, True, color)
            screen.blit(text, (50, 100 + i * 40))
        
        for i, bg in enumerate(background_names):
            color = RED if i == selected_background else BLACK
            text = font.render(bg, True, color)
            screen.blit(text, (250, 100 + i * 40))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_difficulty = (selected_difficulty - 1) % len(difficulties)
                if event.key == pygame.K_DOWN:
                    selected_difficulty = (selected_difficulty + 1) % len(difficulties)
                if event.key == pygame.K_LEFT:
                    selected_background = (selected_background - 1) % len(background_names)
                if event.key == pygame.K_RIGHT:
                    selected_background = (selected_background + 1) % len(background_names)
                if event.key == pygame.K_RETURN:
                    return difficulties[selected_difficulty], BACKGROUND_COLORS[background_names[selected_background]]

# Основна функція гри
def game(difficulty, background_color):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()
    
    pacman = pygame.Rect(WIDTH // 2, HEIGHT // 2, CELL_SIZE, CELL_SIZE)
    pacman_speed = 5 if difficulty == "Easy" else 10 if difficulty == "Medium" else 15
    dx, dy = 0, 0
    
    ghosts = [pygame.Rect(random.randint(0, COLS - 1) * CELL_SIZE, random.randint(0, ROWS - 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE) for _ in range(3)]
    ghost_speed = 2 if difficulty == "Easy" else 4 if difficulty == "Medium" else 6
    
    running = True
    while running:
        screen.fill(background_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx, dy = -pacman_speed, 0
                if event.key == pygame.K_RIGHT:
                    dx, dy = pacman_speed, 0
                if event.key == pygame.K_UP:
                    dx, dy = 0, -pacman_speed
                if event.key == pygame.K_DOWN:
                    dx, dy = 0, pacman_speed
        
        pacman.x += dx
        pacman.y += dy
        
        # Обмеження руху Pac-Man
        pacman.x = max(0, min(WIDTH - CELL_SIZE, pacman.x))
        pacman.y = max(0, min(HEIGHT - CELL_SIZE, pacman.y))
        
        pygame.draw.rect(screen, YELLOW, pacman)
        
        # Рух привидів
        for ghost in ghosts:
            ghost.x += random.choice([-ghost_speed, ghost_speed])
            ghost.y += random.choice([-ghost_speed, ghost_speed])
            ghost.x = max(0, min(WIDTH - CELL_SIZE, ghost.x))
            ghost.y = max(0, min(HEIGHT - CELL_SIZE, ghost.y))
            pygame.draw.rect(screen, RED, ghost)
            
            if pacman.colliderect(ghost):
                running = False  # Програш
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    difficulty, background_color = menu()
    game(difficulty, background_color)
