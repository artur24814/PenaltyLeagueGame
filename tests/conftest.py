import pytest

from src.setup import get_teams
from src.factories.season_factory import SeasonFactory
from src.models.orm_fields import IntergerField, RealField, TextField
from .testing_models import TestModel


@pytest.fixture
def teams():
    return get_teams()


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
