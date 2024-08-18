from src.ui_components.colors import RED
from src.settings import WINDOW_HEIGHT, WINDOW_WIDTH


class GoalKeeper:
    def __init__(self, width=None, height=None):
        self.width = width
        self.height = height
        self.center_x, self.center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 90

    def draw(self, pygame, screen, end_x, end_y):
        pygame.draw.line(screen, RED, (self.center_x, self.center_y), (end_x, end_y), 5)
        pygame.draw.circle(screen, RED, (int(end_x), int(end_y)), 10)
