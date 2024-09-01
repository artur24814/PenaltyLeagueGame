from .abstract import StaticGameSprite


class Logo(StaticGameSprite):
    def __init__(self, pos, image_path, size=(25, 25)):
        super().__init__(pos, image_path, size)

    def _get_rect(self):
        return self.image.get_rect(topleft=self.pos)
