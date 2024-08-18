import random
from .abstract import PenaltyState


class DefendingPenaltyState(PenaltyState):
    def resolve_turn(self, player_team_points, oponent_team_points):
        self.oponent_choice = random.randint(0, 8)

        if self.player_choice == self.oponent_choice:
            self.result_message = "Obroniłeś!"
        elif self.player_choice != self.oponent_choice:
            self.result_message = "Przeciwnik strzelił!"
            oponent_team_points += 1

        self.attempts += 1
        self.end_turn = True
        return player_team_points, oponent_team_points

    def update_player_choice(self, choice):
        pass

    def draw(self, pygame, screen, *args, **kwargs):
        pass
