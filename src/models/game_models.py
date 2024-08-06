import random

from src.models.orm_models import Model


class FootballClub(Model):
    accident_events = [-15, -13, -11, -9, -7, -5, -3, -1, 0, 1, 3, 5, 7, 9, 11, 13, 15]
    db_fields_to_lookup = ['_id', 'title', 'potential', 'logo', 'points', 'mood', 'games', 'wins', 'draws', 'losses']

    def __init__(self, title=None, potential=None, logo=None, points=0, mood=5, games=0, wins=0, draws=0, losses=0):
        super().__init__()
        self.title = title
        self.potential = potential
        self.logo = logo
        self.points = points
        self.mood = mood

        self.games = games
        self.wins = wins
        self.draws = draws
        self.losses = losses

    @property
    def min_mood(self):
        return 5

    @property
    def max_mood(self):
        return 20

    def get_shape(self):
        return self.potential + self.mood + random.choice(self.accident_events)

    def set_potential(self, new_potential):
        self.potential = new_potential

    def set_points(self, points):
        self._set_stats(points)
        self._set_mood(self.translate_points_to_mood(points))
        self.points += points

    def _set_stats(self, points):
        if points == 3:
            self.wins += 1
        elif points == 0:
            self.losses += 1
        else:
            self.draws += 1
        return

    def _set_mood(self, value):
        if self._is_between_normal_mood():
            self.mood += value
        elif self._is_below_normal_mood_but_the_match_result_positive(value):
            self.mood += value
        elif self._is_above_normal_mood_but_the_match_result_negative(value):
            self.mood += value
        else:
            pass

    def translate_points_to_mood(self, points):
        return 3 if points == 3 else (-1 if points else 1)

    def _is_between_normal_mood(self):
        return self.min_mood < self.mood < self.max_mood

    def _is_below_normal_mood_but_the_match_result_positive(self, value):
        return self.mood <= self.min_mood and value > 0

    def _is_above_normal_mood_but_the_match_result_negative(self, value):
        return self.mood >= self.max_mood and value < 0

    def __str__(self) -> str:
        return f'{self.title} - {self.potential}'

    def __eq__(self, other):
        return self.title == other.title

    def __ne__(self, other):
        return self.title != other.title

    def __hash__(self):
        return hash((self.title, ))


class Season(Model):
    db_fields_to_lookup = ['_id', 'end']

    def __init__(self, match_weeks=None, end=False):
        super().__init__()
        self.match_weeks = match_weeks
        self.end = end
        self.index = 0

    @property
    def get_match_weeks(self):
        return MatchWeek.manager.filter(season_id=self._id).execute()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.match_weeks[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result

    def __len__(self):
        return len(self.match_weeks)

    def create(self, *args, **kwargs):
        self._id = super().create(*args, **kwargs).execute()
        for match_week in self.match_weeks:
            match_week.season_id = self._id
            match_week._id = match_week.create().execute()
            for match in match_week:
                match.match_week_id = match_week._id
                match._id = match.create().execute()
        return self._id


class MatchWeek(Model):
    db_fields_to_lookup = ['_id', 'season_id', 'number', 'end']

    def __init__(self, season_id=-1, number=0, end=False):
        super().__init__()
        self.season_id = season_id
        self.matches = []
        self.number = number
        self.end = end
        self.index = 0

    @property
    def get_matches(self):
        return Match.manager.filter(match_week_id=self._id).execute()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.matches[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result


class Match(Model):
    db_fields_to_lookup = ['_id', 'club_home', 'club_away', 'match_week_id', 'played']

    def __init__(self, club_home=0, club_away=1, match_week_id=-1, played=False):
        super().__init__()
        self.club_home = club_home
        self.club_away = club_away
        self.match_week_id = match_week_id
        self.played = played

    @property
    def get_club_home(self):
        if isinstance(self.club_home, int):
            return FootballClub.manager.get_one(_id=self.club_home).execute()
        return self.club_home

    @property
    def get_club_away(self):
        if isinstance(self.club_away, int):
            return FootballClub.manager.get_one(_id=self.club_away).execute()
        return self.club_away

    def create(self, *args, **kwargs):
        if not isinstance(self.club_home, int) or not isinstance(self.club_away, int):
            self.club_home = self.club_home.id
            self.club_away = self.club_away.id
        return super().create(*args, **kwargs)

    def end_match(self):
        self._set_match_as_played()
        points_home, points_away = self._get_points_after_match()
        self.club_home.set_points(points_home)
        self.club_away.set_points(points_away)

    def _set_match_as_played(self):
        self.played = True

    def _get_points_after_match(self):
        shape_home = self.club_home.get_shape()
        shape_away = self.club_away.get_shape()
        return 3, 0 if shape_home > shape_away else (0, 3 if shape_home > shape_away else 1, 1)

    def __str__(self) -> str:
        return f'{self.club_home} vs. {self.club_away}'

    def __eq__(self, other):
        return hash(frozenset(self.__dict__.items()))

    def __ne__(self, other):
        return self.club_home != other.club_home or self.club_away != other.club_away
