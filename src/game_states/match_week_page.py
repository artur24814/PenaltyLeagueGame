import os

from src.game_states.abstract import GameState
from src.game_states.penalty_game_page import PenaltyGamePage
from src.ui_components.colors import BLACK, GREEN, GRAY
from src.models.game_models import MatchWeek
from src.ui_components.buttons.base_button import BaseBtn
from src.settings import WINDOW_HEIGHT, WINDOW_WIDTH, BASE_DIR
from src.services import generate_results_and_save_matches


class MatchWeekPage(GameState):
    def __init__(self, game, pygame, screen):
        super().__init__(game, pygame, screen)
        self.font = self.pygame.font.Font(None, 36)
        self.small_font = self.pygame.font.Font(None, 28)
        self.matchWeek = MatchWeek.query_creator.filter(end=False).execute()[0]
        self.matches = self.matchWeek.get_matches
        self.button_next = BaseBtn(width=300, height=50, font=self.font, text="Go to match ->")
        self.button_random = BaseBtn(width=300, height=50, font=self.font, text="Simulate results")

    def get_buttons(self):
        return (
            (
                self.button_next,
                lambda: self.game.change_state(PenaltyGamePage(self.game, self.pygame, self.screen, self.matchWeek.id))
            ),
            (
                self.button_random,
                lambda: self.play_matches()
            ),
        )

    def play_matches(self):
        self.matchWeek.end = 1
        generate_results_and_save_matches(matches=self.matches)
        self.matchWeek.save().execute()
        from src.game_states.season_page import SeasonPage
        self.game.change_state(SeasonPage(self.game, self.pygame, self.screen))

    def update(self):
        pass

    def draw(self):
        background_image = self.pygame.image.load(os.path.join(BASE_DIR, 'assets', 'img', 'match-weak-background.jpeg'))
        background_image = self.pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(background_image, (0, 0))
        self.draw_matches()
        self.button_next.draw(
            screen=self.screen,
            x=((WINDOW_WIDTH) - self.button_next.width) - 10,
            y=(WINDOW_HEIGHT - self.button_next.height) - 10
        )
        self.button_random.draw(
            screen=self.screen,
            x=((WINDOW_WIDTH) - (self.button_next.width + self.button_random.width)) - 20,
            y=(WINDOW_HEIGHT - self.button_random.height) - 10
        )
        self.pygame.display.flip()

    def draw_matches(self):
        start_y = 100
        spacing_y = 50
        circle_radius = 10

        for match in self.matches:
            circle_color = GREEN if match.played else GRAY
            self.pygame.draw.circle(self.screen, circle_color, (50, start_y + circle_radius), circle_radius)
            match_text = f"{match.get_club_home.title} - {match.get_club_away.title}"
            text_surface = self.small_font.render(match_text, True, BLACK)
            self.screen.blit(text_surface, (70, start_y))
            start_y += spacing_y
