import json

from .models.game_models import FootballClub, Season
from .factories.season_factory import SeasonFactory
from .settings import TEAMS_CONFIG_FILE_DIR, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_NAME


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
            new_team = FootballClub(title=team_name, potential=values.get('potential'), logo=values.get('logo'), computer=values.get('computer'))
            new_team._id = new_team.save().execute(testing)
            teams.append(new_team)
    else:
        teams = [team for team in result]

    return teams


def get_current_season(testing=False):
    if (existing_unfinished_season := Season.query_creator.get_one(end=0).execute()):
        return existing_unfinished_season
    factory = SeasonFactory(teams=get_or_create_teams())
    new_season = factory.get_new_season()
    new_season.save()
    return new_season


def validate_team_config(team_config):
    if (len(team_config) % 2) != 0:
        raise ValueError('There should be an even number of teams')


def pygame_init():
    import pygame

    # Inicjalizacja pygame
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_NAME)

    return pygame, screen
