import json
from .models.game_models import FootballClub
from .settings import TEAMS_CONFIG_FILE_DIR


def get_teams_config(path=TEAMS_CONFIG_FILE_DIR):
    with open(path) as file:
        data_dict = json.load(file)
        return data_dict


def get_teams():
    team_config = get_teams_config()
    validate_team_config(team_config)

    teams = []

    id_indx = 1
    for team_name, values in team_config.items():
        new_club = FootballClub(team_name, values.get('potential'), values.get('logo'))
        new_club.id = id_indx
        id_indx += 1
        teams.append(new_club)

    return teams


def get_or_create_teams(testing=False):
    team_config = get_teams_config()
    validate_team_config(team_config)

    teams = []
    result = FootballClub.manager.all().execute(testing)

    if result == []:
        for team_name, values in team_config.items():
            new_team = FootballClub(team_name, values.get('potential'), values.get('logo'))
            new_team._id = new_team.create().execute(testing)
            teams.append(new_team)
    else:
        teams = [team for team in result]

    return teams


def validate_team_config(team_config):
    if (len(team_config) % 2) != 0:
        raise ValueError('There should be an even number of teams')
