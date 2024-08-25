from .abstract import StaticGameSprite
from src.settings import WINDOW_HEIGHT, WINDOW_WIDTH


class Pitch(StaticGameSprite):
    def __init__(self, pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70), image_path=['assets', 'img', 'pitch.png'], size=(WINDOW_WIDTH, 480)):
        super().__init__(pos, image_path, size)

    def _get_rect(self):
        return self.image.get_rect(midtop=self.pos)
