import random

from models.game_models import MatchWeek, Match, Season


class SeasonFactory:
    def __init__(self, clubs):
        self.clubs = clubs
        self.match_weeks_amount_half_season = (len(self.clubs) - 1) * 2
        self.match_weeks_amount_season = self.match_weeks_amount_half_season * 2

        self.season_legs = []

    def get_new_season(self):
        half_seasons_matches_generator = self._generator_match_weeks_for_half_season()
        all_seasons_week_matches = self._convert_from_half_season_weeks_into_all_season_weeks(half_seasons_matches_generator)
        return Season(match_weeks=all_seasons_week_matches)

    def _generator_match_weeks_for_half_season(self):
        """
        Creating an unique collections of list of pair items from a list.
        First shuffling a list_items and took first two items,
        Check if this pair of items not in this list `witch appending now`, then check if not in a main `list_tours`
        if not add to list `witch appending now` and if length of this list / 2 add this list to the main `list_tours`
        otherwase shuffle again ang check again.
        """
        legs_counter = 1
        half_season_legs = []

        while legs_counter <= self.match_weeks_amount_half_season:
            one_leg = []
            random.shuffle(self.clubs)

            randomed_list = self.clubs.copy()

            while self._is_number_of_matches_in_leg_less_than_half_of_teams_on_list_and_still_teams_left(one_leg, randomed_list):
                # create pair
                match = (randomed_list[0], randomed_list[1])

                if self._is_this_match_not_already_in_the_leg_and_it_is_not_last_two_teams(match, one_leg, randomed_list):
                    if not self._is_match_already_exist(match, half_season_legs):
                        one_leg.append(match)
                        del randomed_list[0:2]

                # if only 2 items left in the list
                if len(randomed_list) == 2:
                    one_leg.append((randomed_list.pop(), randomed_list.pop()))
                random.shuffle(randomed_list)

            half_season_legs.append(one_leg)
            legs_counter += 1

        return half_season_legs

    def _is_number_of_matches_in_leg_less_than_half_of_teams_on_list_and_still_teams_left(self, leg, randomed_list):
        return len(leg) <= (len(self.clubs) / 2) and len(randomed_list) >= 2

    def _is_this_match_not_already_in_the_leg_and_it_is_not_last_two_teams(self, match, leg, randomed_list):
        return match not in leg and len(randomed_list) != 2

    def _is_match_already_exist(self, match, temp_season_legs):
        for elements in temp_season_legs:
            if match in elements:
                return True
        return False

    def _convert_from_half_season_weeks_into_all_season_weeks(self, half_season_legs):
        for index, legs in enumerate(half_season_legs, start=1):
            # first half season
            self.season_legs.append(self._create_match_week_objects(legs, index))
            # second half season
            self.season_legs.append(self._create_match_week_objects(legs, self.match_weeks_amount_half_season + index, reverse=True))
        return self.season_legs

    def _create_match_week_objects(self, leg_list, legs_counter, reverse=False):
        match_week = MatchWeek(number=legs_counter)
        for match_tuple in leg_list:
            match_obj = Match(club_home=match_tuple[0], club_away=match_tuple[1]) if not reverse \
                else Match(club_home=match_tuple[1], club_away=match_tuple[0])
            match_week.matches.append(match_obj)

        return match_week
