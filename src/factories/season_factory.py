import random

from src.models.game_models import MatchWeek, Match, Season


class SeasonFactory:
    def __init__(self, teams):
        self.teams = teams
        self.match_weeks_amount_half_season = (len(self.teams) - 1) * 2
        self.match_weeks_amount_season = self.match_weeks_amount_half_season * 2

        self.season_legs = []

    def get_new_season(self):
        half_seasons_matches_generator = self._list_of_unique_match_pair_tuples()
        all_seasons_week_matches = self._convert_from_match_weeks_tuples_into_match_weeks_objs(half_seasons_matches_generator)
        return Season(match_weeks=all_seasons_week_matches)

    def _list_of_unique_match_pair_tuples(self):
        """
        Creating an unique collections of list of pair items from a list.
        """
        legs_counter = 1
        list_of_match_tuples = []

        while legs_counter <= self.match_weeks_amount_half_season:
            one_leg = []
            random.shuffle(self.teams)

            randomed_list = self.teams.copy()

            while self._is_number_of_matches_in_leg_less_than_half_of_teams_on_list_and_still_teams_left(one_leg, randomed_list):
                # create teams pair
                match = (randomed_list[0], randomed_list[1])

                if self._is_this_match_not_already_in_the_leg_and_it_is_not_last_two_teams(match, one_leg, randomed_list):
                    if not self._is_match_already_exist(match, list_of_match_tuples):
                        one_leg.append(match)
                        del randomed_list[0:2]

                # if only 2 items left in the list
                if len(randomed_list) == 2:
                    one_leg.append((randomed_list.pop(), randomed_list.pop()))
                random.shuffle(randomed_list)

            list_of_match_tuples.append(one_leg)
            legs_counter += 1

        return list_of_match_tuples

    def _is_number_of_matches_in_leg_less_than_half_of_teams_on_list_and_still_teams_left(self, leg, randomed_list):
        return len(leg) <= (len(self.teams) / 2) and len(randomed_list) >= 2

    def _is_this_match_not_already_in_the_leg_and_it_is_not_last_two_teams(self, match, leg, randomed_list):
        return match not in leg and len(randomed_list) != 2

    def _is_match_already_exist(self, match, temp_season_legs):
        for elements in temp_season_legs:
            if match in elements:
                return True
        return False

    def _convert_from_match_weeks_tuples_into_match_weeks_objs(self, list_of_match_tuples):
        for index, legs in enumerate(list_of_match_tuples, start=1):
            self.season_legs.append(self._create_match_week_objects(legs, index))
        return self.season_legs

    def _create_match_week_objects(self, leg_list, legs_counter, reverse=False):
        match_week = MatchWeek(number=legs_counter)
        for match_tuple in leg_list:
            match_obj = Match(club_home=match_tuple[0], club_away=match_tuple[1]) if not reverse \
                else Match(club_home=match_tuple[1], club_away=match_tuple[0])
            match_week.matches.append(match_obj)

        return match_week
