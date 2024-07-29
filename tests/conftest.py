import pytest

from src.setup import get_teams
from src.factories.season_factory import SeasonFactory


@pytest.fixture
def teams():
    return get_teams()


@pytest.fixture
def season(teams):
    gen = SeasonFactory(teams=teams)
    new_season = gen.get_new_season()
    return new_season
