from src.ui_components.abstract import Element


class Table(Element):
    def __init__(self, data=None, headers=None, fields=None, spacing_x=100, spacing_y=50, font=None, color=None):
        self.data = data
        self.headers = headers
        self.fields = fields
        self.spacing_x = spacing_x
        self.spacing_y = spacing_y
        self.font = font
        self.color = color

    def draw(self, screen, x, y):
        self.draw_headers(screen, x, y)
        self.draw_body(screen, x, y)

    def draw_headers(self, screen, x, y):
        ...

    def draw_body(self, screen, x, y):
        ...
