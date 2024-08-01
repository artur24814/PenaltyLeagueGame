from src.models.game_models import FootballClub


def test_blank_database(testing_database):
    result = FootballClub.manager.all().execute(testing=True)
    assert len(result) == 0


def test_full_database(testing_database, teams_objs):
    result = FootballClub.manager.all().execute(testing=True)
    assert len(result) == 8


def test_few_result(testing_database, teams_objs):
    result = FootballClub.manager.filter(potential=14).execute(testing=True)
    assert len(result) == 2


def test_one_result(testing_database, teams_objs):
    result = FootballClub.manager.get_one(potential=20).execute(testing=True)
    assert isinstance(result, FootballClub) is True


def test_delete(testing_database, teams_objs):
    team = FootballClub.manager.get_one(potential=20).execute(testing=True)
    assert team.delete().execute(testing=True) == 0
    result = FootballClub.manager.all().execute(testing=True)
    assert len(result) == 7
