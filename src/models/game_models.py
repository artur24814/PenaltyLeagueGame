import random

from src.models.orm_models import Model


class FootballClub(Model):
    accident_events = [-15, -13, -11, -9, -7, -5, -3, -1, 0, 1, 3, 5, 7, 9, 11, 13, 15]

    def __init__(self, title=None, potential=None, logo=None, points=0, mood=5):
        super().__init__()
        self.title = title
        self.potential = potential
        self.logo = logo
        self.points = points
        self.mood = mood

        self.games = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0

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
            self.win += 1
        elif points == 0:
            self.lose += 1
        else:
            self.draw += 1

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


class Season:
    def __init__(self, match_weeks):
        self._id = -1
        self.match_weeks = match_weeks
        self.index = 0

    @property
    def id(self):
        return self._id

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


class MatchWeek:
    def __init__(self, number, end=False):
        self._id = -1
        self.matches = []
        self.number = number
        self.end = end
        self.index = 0

    @property
    def id(self):
        return self._id

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.matches[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result


class Match:
    def __init__(self, club_home: FootballClub, club_away: FootballClub, week=None, played=False):
        self._id = -1
        self.club_home = club_home
        self.club_away = club_away
        self.matchWeek = week
        self.played = played

    @property
    def id(self):
        return self._id

    def set_match_as_played(self):
        self.played = True

    def end_match(self):
        self.set_match_as_played()
        points_home, points_away = self._get_points_after_match()
        self.club_home.set_points(points_home)
        self.club_away.set_points(points_away)

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
