# main.py
import pygame
import sys
import toml
from screens.welcome_screen import WelcomeScreen
from screens.customize_screen import CustomizeScreen
from screens.game_screen import main_game
from enemy import Enemy

# Load patterns from the TOML file
with open("patterns.toml", "r") as file:
    patterns = toml.load(file)

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Create Pygame screen
screen = pygame.display.set_mode((800, 600))
welcome_screen = WelcomeScreen()

while True:
    choice = welcome_screen.run()

    if choice == "start":
        # Start the game
        main_game(screen, clock, level=1)
    elif choice == "customize":
        customize_screen = CustomizeScreen()
        customize_screen.run()
