import os
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent
TEAMS_CONFIG_FILE = 'teams.config.json'
TEAMS_CONFIG_FILE_DIR = os.path.join(BASE_DIR, TEAMS_CONFIG_FILE)
