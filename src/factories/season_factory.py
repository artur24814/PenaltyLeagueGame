from src.models.game_models import MatchWeek, Match, Season


class SeasonFactory:
    def __init__(self, teams):
        self.teams = teams
        self.rounds_in_half_season = len(self.teams) - 1
        self.total_rounds = self.rounds_in_half_season * 2
        self.match_weeks = []

    def get_new_season(self):
        round_robin_schedule = self._generate_round_robin_schedule()
        full_season_matches = self._create_full_season_schedule(round_robin_schedule)
        return Season(match_weeks=full_season_matches)

    def _generate_round_robin_schedule(self):
        """
        Generate a round-robin schedule where each team plays with every other team once.
        """
        teams = self._ensure_even_number_of_teams()
        schedule = []

        for _ in range(1, self.rounds_in_half_season + 1):
            current_round_matches = self._generate_matches_for_round(teams)
            schedule.append(current_round_matches)
            teams = self._rotate_teams(teams)

        return schedule

    def _ensure_even_number_of_teams(self):
        return self.teams

    def _generate_matches_for_round(self, teams):
        return [
            (teams[i], teams[-i - 1])
            for i in range(len(teams) // 2)
            if teams[i] is not None and teams[-i - 1] is not None
        ]

    def _rotate_teams(self, teams):
        return [teams[0]] + [teams[-1]] + teams[1:-1]

    def _create_full_season_schedule(self, round_robin_schedule):
        self.match_weeks = []

        # First half of the season (normal order)
        for round_number, matches in enumerate(round_robin_schedule, start=1):
            self.match_weeks.append(self._create_match_week(matches, round_number))

        # Second half of the season (reversed order)
        for round_number, matches in enumerate(round_robin_schedule, start=self.rounds_in_half_season + 1):
            self.match_weeks.append(self._create_match_week(matches, round_number, reverse=True))

        return self.match_weeks

    def _create_match_week(self, matches, round_number, reverse=False):
        match_week = MatchWeek(number=round_number)
        for home, away in matches:
            if reverse:
                home, away = away, home
            match_week.matches.append(Match(club_home=home, club_away=away))

        return match_week
