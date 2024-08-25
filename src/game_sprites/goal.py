from .abstract import StaticGameSprite
from src.settings import WINDOW_HEIGHT, WINDOW_WIDTH


class Goal(StaticGameSprite):
    def __init__(self, pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 15), image_path=['assets', 'img', 'goal', '1.png'], size=(430, 220)):
        super().__init__(pos, image_path, size)
