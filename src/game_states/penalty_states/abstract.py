class PenaltyState:
    def __init__(self, state_text=''):
        self.state_text = state_text
        self.attempts = 0
        self.result_message = ""
        self.player_choice = 0
        self.oponent_choice = 0
        self.end_turn = False

    def resolve_turn(self, player_team_points, oponent_team_points) -> tuple:
        ...
