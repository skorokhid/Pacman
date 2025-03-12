import pygame

pygame.init()
pygame.mixer.init()

# Ініціалізація шрифту
font = pygame.font.Font(None, 36)

# Перевірка доступності звуку
SOUND_ENABLED = pygame.mixer.get_init() is not None