from src.setup import get_teams_config
from src.models.game_models import FootballClub


def test_teams_length(teams):
    teams_dict = get_teams_config()
    assert len(teams) == len(teams_dict)


def test_teams_creating(teams):
    for team in teams:
        assert isinstance(team, FootballClub)
