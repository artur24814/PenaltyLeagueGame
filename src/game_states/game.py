from src.game_states.welcome_page import WelcomePage


class Game:
    def __init__(self, pygame, screen):
        self.pygame = pygame
        self.screen = screen
        self.state = WelcomePage(self, self.pygame, self.screen)

    def change_state(self, new_state):
        self.state = new_state

    def run(self):
        while True:
            events = self.pygame.event.get()
            self.state.handle_events(events)
            self.state.update()
            self.state.draw()
