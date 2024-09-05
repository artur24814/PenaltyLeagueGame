import pytest
import os

from src.setup import get_teams_config, get_or_create_teams
from src.db.db_init import run_init_queryes, BASE_DIR
from src.factories.season_factory import SeasonFactory
from src.models.orm_fields import IntergerField, RealField, TextField
from src.models.game_models import FootballClub

from .testing_models import TestModel


@pytest.fixture(autouse=True)
def setup_test_env():
    from src.settings import set_testing_mode
    set_testing_mode(True)
    return True


@pytest.fixture(scope="session", autouse=True)
def session_teardown():
    yield
    temp_file = os.path.join(BASE_DIR.parent, 'test-db.db')
    if os.path.exists(temp_file):
        os.remove(temp_file)


@pytest.fixture
def testing_database():
    from src.settings import TESTING
    print(TESTING)
    file_path = os.path.join(BASE_DIR, 'models', 'game_models.py')
    run_init_queryes(file_path, TESTING)
    return


@pytest.fixture
def teams():
    team_config = get_teams_config()

    teams = []

    id_indx = 1
    for team_name, values in team_config.items():
        new_club = FootballClub(title=team_name, potential=values.get('potential'), logo=values.get('logo'))
        new_club.id = id_indx
        id_indx += 1
        teams.append(new_club)

    return teams


@pytest.fixture
def teams_objs():
    return get_or_create_teams(testing=True)


@pytest.fixture
def season(teams):
    gen = SeasonFactory(teams=teams)
    new_season = gen.get_new_season()
    return new_season


@pytest.fixture
def test_model():
    t_model = TestModel(name='Harry', second='Potter', last=2)
    return t_model


@pytest.fixture
def integer_field():
    return IntergerField(name='test_integer', null=False, primary=False)


@pytest.fixture
def text_field():
    return TextField(name='test_text', null=False, primary=False)


@pytest.fixture
def real_field():
    return RealField(name='test_real', null=False, primary=False)
