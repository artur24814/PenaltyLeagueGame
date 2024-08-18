import random
from .abstract import PenaltyState
from src.ui_components.colors import GREEN
from src.settings import WINDOW_HEIGHT, WINDOW_WIDTH


class ShootingPenaltyState(PenaltyState):
    def resolve_turn(self, player_team_points, oponent_team_points):
        self.oponent_choice = random.randint(0, 8)

        if self.player_choice == self.oponent_choice:
            self.result_message = "Nie trafiłeś!"
        elif self.player_choice != self.oponent_choice:
            self.result_message = "Strzeliłeś!"
            player_team_points += 1

        self.attempts += 1
        self.end_turn = True
        return player_team_points, oponent_team_points

    def update_player_choice(self, choice):
        self.player_choice = choice

    def draw(self, pygame, screen, arrow_end):
        center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 200
        pygame.draw.line(screen, GREEN, (center_x, center_y), arrow_end, 3)
