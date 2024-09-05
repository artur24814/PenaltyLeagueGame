import random
from typing import Optional
from dataclasses import dataclass, field

from src.models.orm_models import Model


@dataclass
class FootballClub(Model):
    accident_events = [-15, -13, -11, -9, -7, -5, -3, -1, 0, 1, 3, 5, 7, 9, 11, 13, 15]
    db_fields_to_lookup = ['_id', 'title', 'potential', 'logo', 'points', 'mood', 'games', 'wins', 'draws', 'losses', 'computer']
    title: Optional[str] = field(default=None)
    potential: Optional[int] = field(default=None)
    logo: Optional[str] = field(default=None)
    points: int = field(default=0)
    mood: int = field(default=5)

    games: int = field(default=0)
    wins: int = field(default=0)
    draws: int = field(default=0)
    losses: int = field(default=0)
    computer: int = field(default=1)

    @property
    def min_mood(self):
        return 5

    @property
    def max_mood(self):
        return 20

    def get_shape(self):
        return int(self.potential) + int(self.mood) + random.choice(self.accident_events)

    def set_potential(self, new_potential):
        self.potential = new_potential

    def set_points(self, points):
        self._set_stats(points)
        self._set_mood(self.translate_points_to_mood(points))
        self.points += points
        return self

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


@dataclass
class Season(Model):
    db_fields_to_lookup = ['_id', 'end']
    match_weeks: Optional[list] = field(default=None)
    end: bool = field(default=False)
    index: int = field(default=0)

    @property
    def get_match_weeks(self):
        return MatchWeek.query_creator.filter(season_id=self._id).execute()

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
        return len(self.get_match_weeks) if not self.match_weeks else len(self.match_weeks)

    def save(self, *args, **kwargs):
        self._id = super().save(*args, **kwargs).execute()
        for match_week in self.match_weeks:
            match_week.season_id = self._id
            match_week._id = match_week.save().execute()
            for match in match_week:
                match.match_week_id = match_week._id
                match._id = match.save().execute()
        return self._id


@dataclass
class MatchWeek(Model):
    db_fields_to_lookup = ['_id', 'season_id', 'number', 'end']

    season_id: int = field(default=-1)
    matches: list = field(default_factory=list)
    number: int = field(default=0)
    end: bool = field(default=False)
    index: int = field(default=0)

    @property
    def get_matches(self):
        return Match.query_creator.filter(match_week_id=self._id).execute()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.matches[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result


@dataclass
class Match(Model):
    db_fields_to_lookup = ['_id', 'club_home', 'club_away', 'match_week_id', 'played']

    club_home: int = field(default=0)
    club_away: int = field(default=1)
    match_week_id: int = field(default=-1)
    played: bool = field(default=False)

    @property
    def get_club_home(self):
        if isinstance(self.club_home, int):
            return FootballClub.query_creator.get_one(_id=self.club_home).execute()
        return self.club_home

    @property
    def get_club_away(self):
        if isinstance(self.club_away, int):
            return FootballClub.query_creator.get_one(_id=self.club_away).execute()
        return self.club_away

    def save(self, *args, **kwargs):
        club_home_obj = self.get_club_home
        club_away_obj = self.get_club_away
        if not isinstance(self.club_home, int) or not isinstance(self.club_away, int):
            self.club_home = club_home_obj.id
            self.club_away = club_away_obj.id

        if kwargs.get('save_instance', None):
            return super().save(*args, **kwargs)
        club_home_obj.save().execute()
        club_away_obj.save().execute()
        return super().save(*args, **kwargs)

    def end_match(self):
        self._set_match_as_played()
        points_home, points_away = self._get_points_after_match()
        self.club_home = self.get_club_home.set_points(points_home)
        self.club_away = self.get_club_away.set_points(points_away)

    def _set_match_as_played(self):
        self.played = True

    def _get_points_after_match(self):
        shape_home = self.get_club_home.get_shape()
        shape_away = self.get_club_away.get_shape()
        return (3, 0) if shape_home > shape_away else ((0, 3) if shape_home > shape_away else (1, 1))

    def __str__(self) -> str:
        return f'{self.club_home} vs. {self.club_away}'

    def __eq__(self, other):
        return hash(frozenset(self.__dict__.items()))

    def __ne__(self, other):
        return self.club_home != other.club_home or self.club_away != other.club_away
