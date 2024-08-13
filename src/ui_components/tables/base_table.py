from .abstract import Table


class BaseTable(Table):

    def draw_headers(self, screen, x, y):
        for i, title in enumerate(self.headers):
            text_surface = self.font.render(title, True, self.color)
            screen.blit(text_surface, (x + i * self.spacing_x, y))

    def draw_body(self, screen, x, y):
        for row in self.data:
            y += self.spacing_y
            for index, field in enumerate(self.fields):
                text_surface = self.font.render(str(getattr(row, field)), True, self.color)
                screen.blit(text_surface, (x + index * self.spacing_x, y))
