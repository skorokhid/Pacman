from constants import WHITE, font

class ScoreManager:
    def __init__(self):
        self.score = 0

    def draw(self, screen):
        score_text = font.render(f"score:{self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))