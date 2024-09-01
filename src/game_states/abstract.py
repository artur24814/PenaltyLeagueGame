import sys
import os

from src.settings import WINDOW_HEIGHT, WINDOW_WIDTH, BASE_DIR


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
            self.custome_events(event)

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

    def custome_events(self, event):
        pass

    def get_buttons(self):
        return ()

    def update(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def draw_background_image(self, path_dir_list, pos=(0, 0), size=(WINDOW_WIDTH, WINDOW_HEIGHT)):
        background_image = self.pygame.image.load(os.path.join(BASE_DIR, *path_dir_list))
        background_image = self.pygame.transform.scale(background_image, size)
        self.screen.blit(background_image, pos)

    def is_end_state(self):
        return False

    def run_end_state(self):
        pass
