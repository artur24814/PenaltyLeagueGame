from src.setup import pygame_init
from src.game_states.game import Game

# Inicjalizacja pygame
pygame, screen = pygame_init()


if __name__ == "__main__":
    game = Game(pygame, screen)
    game.run()
