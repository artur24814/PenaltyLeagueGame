import json
from .models.game_models import FootballClub
from .settings import TEAMS_CONFIG_FILE_DIR


def get_teams_config(path=TEAMS_CONFIG_FILE_DIR):
    with open(path) as file:
        data_dict = json.load(file)
        return data_dict


def get_teams():
    team_config = get_teams_config()

    if (len(team_config) % 2) != 0:
        raise ValueError('There should be an even number of teams')

    teams = []

    id_indx = 1
    for team_name, values in team_config.items():
        new_club = FootballClub(team_name, values.get('potential'), values.get('logo'))
        print(new_club)
        new_club.id = id_indx
        id_indx += 1
        teams.append(new_club)

    return teams
