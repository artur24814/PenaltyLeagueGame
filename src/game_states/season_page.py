from src.game_states.abstract import GameState
from src.ui_components.colors import WHITE, BLACK
from src.ui_components.tables.ordering_table import OrderingTable
from src.ui_components.buttons.base_button import BaseBtn
from src.models.game_models import FootballClub
from src.game_states.match_week_page import MatchWeekPage
from src.settings import WINDOW_HEIGHT, WINDOW_WIDTH


class SeasonPage(GameState):
    def __init__(self, game, pygame, screen):
        super().__init__(game, pygame, screen)
        self.font = self.pygame.font.Font(None, 36)
        self.small_font = self.pygame.font.Font(None, 28)
        self.teams = FootballClub.query_creator.all().execute()
        self.season_table = OrderingTable(data=self.teams,
                                          headers=["Team", "Points", "Wins", "Draws", "Losses"],
                                          fields=["title", "points", "wins", "draws", "losses"],
                                          color=BLACK,
                                          font=self.small_font,
                                          order_func=lambda e: int(e.points))
        self.button_next = BaseBtn(width=300, height=50, font=self.font, text="Next game ->")

    def get_buttons(self):
        return (
            (
                self.button_next,
                lambda: self.game.change_state(MatchWeekPage(self.game, self.pygame, self.screen))
            ),
        )

    def update(self):
        pass

    def draw(self):
        self.screen.fill(WHITE)
        self.season_table.draw(self.screen, 100, 100)
        self.button_next.draw(
            screen=self.screen,
            x=((WINDOW_WIDTH) - self.button_next.width) - 10,
            y=(WINDOW_HEIGHT - self.button_next.height) - 10
        )
        self.pygame.display.flip()
