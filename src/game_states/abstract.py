import sys


class GameState:
    def __init__(self, game, pygame=None, screen=None):
        self.game = game
        self.pygame = pygame
        self.screen = screen

    def handle_events(self, events):
        for event in events:
            self.exit_event(event)
            if event.type == self.pygame.MOUSEBUTTONDOWN:
                self.button_events(event)

    def exit_event(self, event):
        if event.type == self.pygame.QUIT:
            self.pygame.quit()
            sys.exit()

    def button_events(self, event):
        mouse_pos = event.pos
        for item in self.get_buttons():
            button, func = item
            if button.rect.collidepoint(mouse_pos):
                button.click(func)

    def get_buttons(self):
        return ()

    def update(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError
