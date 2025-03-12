from constants import WHITE, font


class ScoreManager:
    """Клас для керування рахунком у грі."""

    def __init__(self):
        """Ініціалізує рахунок."""
        self.score = 0

    def draw(self, screen):
        """Відображає рахунок на екрані."""
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
