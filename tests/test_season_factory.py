from src.setup import get_teams_config
from src.models.game_models import Match, MatchWeek


def test_season_weeks_length(season):
    teams_dict = get_teams_config()
    assert len(season) == (len(teams_dict) * 2) - 2
    for match_week in season:
        assert (len(teams_dict))/2 == len(match_week.matches)


def test_season_weeks_unique_games(season):
    unique_matches = []
    for match_week in season:
        for match in match_week:
            for unique_match in unique_matches:
                assert match == unique_match
            unique_matches.append(match)


def test_season_weeks_obj_created(season):
    for match_week in season:
        assert isinstance(match_week, MatchWeek)


def test_season_match_obj_created(season):
    for match_week in season:
        for m in match_week:
            assert isinstance(m, Match)
