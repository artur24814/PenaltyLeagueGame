import os

from src.game_states.abstract import GameState
from src.ui_components.colors import BLACK
from src.ui_components.tables.base_table import BaseTable
from src.ui_components.buttons.base_button import BaseBtn
from src.game_sprites.logo import Logo
from src.game_states.match_week_page import MatchWeekPage
from src.settings import WINDOW_HEIGHT, WINDOW_WIDTH, BASE_DIR
from src.setup import get_or_create_teams, get_current_season


class SeasonPage(GameState):
    def __init__(self, game, pygame, screen):
        super().__init__(game, pygame, screen)
        self.font = self.pygame.font.Font(None, 36)
        self.small_font = self.pygame.font.Font(None, 23)
        self.season = get_current_season()
        self.teams = self.init_teams()
        self.all_sprites = self.pygame.sprite.Group()
        self.populate_logos()
        self.season_table = BaseTable(data=self.teams,
                                      spacing_x=83, spacing_y=24,
                                      headers=["Team", "Points", "W", "D", "L"],
                                      fields=["title", "points", "wins", "draws", "losses"],
                                      color=BLACK,
                                      font=self.small_font)
        self.button_next = BaseBtn(width=300, height=50, font=self.font, text="Next game ->")

    def init_teams(self):
        teams = get_or_create_teams()
        teams.sort(key=lambda e: int(e.points))
        teams = teams[::-1]
        return teams

    def populate_logos(self):
        for index, team in enumerate(self.teams):
            club_logo = Logo(pos=(WINDOW_WIDTH - 430, 48 + (24 * index)), image_path=['assets', 'img', 'icons', team.logo])
            self.all_sprites.add(club_logo)

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
        background_image = self.pygame.image.load(os.path.join(BASE_DIR, 'assets', 'img', 'season-background.jpeg'))
        background_image = self.pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(background_image, (0, 0))
        self.season_table.draw(self.screen, WINDOW_WIDTH - 400, 30)
        self.button_next.draw(
            screen=self.screen,
            x=((WINDOW_WIDTH) - self.button_next.width) - 10,
            y=(WINDOW_HEIGHT - self.button_next.height) - 10
        )
        self.all_sprites.draw(self.screen)
        self.pygame.display.flip()
