import json
from .models.game_models import FootballClub, Season
from .factories.season_factory import SeasonFactory
from .settings import TEAMS_CONFIG_FILE_DIR


def get_teams_config(path=TEAMS_CONFIG_FILE_DIR):
    with open(path) as file:
        data_dict = json.load(file)
        return data_dict


def get_or_create_teams(testing=False):
    team_config = get_teams_config()
    validate_team_config(team_config)

    teams = []
    result = FootballClub.query_creator.all().execute(testing)

    if result == []:
        for team_name, values in team_config.items():
            new_team = FootballClub(team_name, values.get('potential'), values.get('logo'))
            new_team._id = new_team.create().execute(testing)
            teams.append(new_team)
    else:
        teams = [team for team in result]

    return teams


def get_current_season(testing=False):
    if (existing_unfinished_season := Season.query_creator.get_one(end=0)):
        return existing_unfinished_season
    factory = SeasonFactory(teams=get_or_create_teams())
    new_season = factory.get_new_season()
    new_season.create()
    return new_season


def validate_team_config(team_config):
    if (len(team_config) % 2) != 0:
        raise ValueError('There should be an even number of teams')
