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

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

enemy = Enemy("Enemy1")
player = Player()

# Create Pygame screen
screen = pygame.display.set_mode((800, 600))
welcome_screen = WelcomeScreen()
choice = "welcome"

while True:
    if choice == "welcome":
        choice = welcome_screen.run()
    elif choice == "start":
        print("is it here?")
        # Start the game
        choice = main_game(screen, clock, player, level=1)
        print(choice + "where we returned from level1")
        print("this is where we returned from maingame")
        #return from loop in game_screen and add logic that looks for player.hp being returned.
    elif choice == "customize":
        customize_screen = CustomizeScreen()
        customize_screen.run()
    elif choice == "customfight":
        choice = main_game(screen, clock, player, level=4)
    elif choice == "level2":
        choice = main_game(screen, clock, player, level=2)
    elif choice == "level3":
        choice = main_game(screen, clock, player, level=3)
    elif choice == "defeat":
        defeat_screen = DefeatScreen()
        choice = defeat_screen.display()
        player.hp = 3
    elif choice == "victory":
        victory_screen = VictoryScreen()
        enemy.hp = 3
