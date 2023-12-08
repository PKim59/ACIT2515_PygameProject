# main.py
import pygame
import sys
import toml
from screens.welcome_screen import WelcomeScreen
from screens.customize_screen import CustomizeScreen
from screens.game_screen import main_game
from enemy import Enemy
from player import Player
from screens.victory_screen import VictoryScreen
from screens.defeat_screen import DefeatScreen

# Load patterns from the TOML file
with open("patterns.toml", "r") as file:
    patterns = toml.load(file)

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

player = Player()
enemy = Enemy()

# Create Pygame screen
screen = pygame.display.set_mode((800, 600))
welcome_screen = WelcomeScreen()

while True:
    choice = welcome_screen.run()

    if choice == "start":
        # Start the game
        main_game(screen, clock, level=1)
        #return from loop in game_screen and add logic that looks for player.hp being returned.
    elif choice == "customize":
        customize_screen = CustomizeScreen()
        customize_screen.run()
    elif choice == "level2":
        main_game(screen, clock, level=2)
    elif choice == "level3":
        main_game(screen, clock, level=3)
    elif player.hp == 0:
        defeat_screen = DefeatScreen()
    elif enemy.hp == 0:
        victory_screen = VictoryScreen()
