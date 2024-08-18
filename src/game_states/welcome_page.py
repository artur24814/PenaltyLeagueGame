import os

from src.game_states.abstract import GameState
from src.game_states.season_page import SeasonPage
from src.ui_components.buttons.start_game_btn import StartGameBtn
from src.settings import BASE_DIR, WINDOW_HEIGHT, WINDOW_WIDTH


class WelcomePage(GameState):
    def __init__(self, game, pygame, screen):
        super().__init__(game, pygame, screen)
        self.font = self.pygame.font.Font(None, 36)
        self.button_welcome = StartGameBtn(width=500, height=100, font=self.font, text="Start Game")

    def get_buttons(self):
        return (
            (
                self.button_welcome,
                lambda: self.game.change_state(SeasonPage(self.game, self.pygame, self.screen))
            ),
        )

    def update(self):
        pass

    def draw(self):
        background_image = self.pygame.image.load(os.path.join(BASE_DIR, 'assets', 'img', 'welcome-background.jpeg'))
        background_image = self.pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(background_image, (0, 0))
        self.button_welcome.draw(screen=self.screen, x=(WINDOW_WIDTH // 2) - self.button_welcome.width // 2, y=WINDOW_HEIGHT // 2)
        self.pygame.display.flip()
