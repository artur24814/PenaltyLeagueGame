import pygame

from .abstract import Button
from src.ui_components.colors import DARK_GRAY, WHITE


class BaseBtn(Button):
    def __init__(self, width=200, height=50, background=DARK_GRAY, color=WHITE, font=None, text=''):
        self.width = width
        self.height = height
        self.background = background
        self.color = color
        self.font = font
        self.text = text
        self.rect = None

    def draw(self, screen, x, y):
        self.rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(screen, self.background, self.rect)
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        return self.rect

    def click(self, func):
        func()
