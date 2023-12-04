# game_screen.py
import pygame
import sys
import toml
from pygame.locals import *
from screens.welcome_screen import WelcomeScreen
from enemy import Enemy
from player import Player

# Constants
FPS = 60
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()

def display_message(screen, message, font_size, duration):
    font = pygame.font.Font(None, font_size)
    text = font.render(message, True, (255, 0, 0))
    rect = text.get_rect(center=(400, 300))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.delay(duration)

def main_game(screen, clock, level=1, custom_pattern=None):
    running = True
    player_health = 3
    enemy_health = 3
    player = Player()

    # Load patterns from the TOML file
    with open("patterns.toml", "r") as file:
        patterns = toml.load(file)

    # Define enemy names
    enemy_names = ["Enemy1", "Enemy2", "Enemy3"]

    # Create Enemy instances and load patterns
    enemies = [Enemy(name) for name in enemy_names]
    for enemy in enemies:
        enemy.load_pattern(patterns)

    # Global variables and constants
    current_turn = 0
    turn_duration = 3000  # 3 seconds in milliseconds
    enemy_pattern_index = 0

    # Draw the player and enemies at the beginning
    screen.fill(WHITE)
    screen.blit(player.image, player.rect)
    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect)
    pygame.display.flip()

    # Wait for a short moment (e.g., 1 second) to display the initial setup
    pygame.time.delay(1000)

    while running:
        screen.fill(WHITE)

        # Draw the player
        screen.blit(player.image, player.rect)

        # Draw the enemies
        for enemy in enemies:
            screen.blit(enemy.image, enemy.rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check if it's the player's turn
        if current_turn % turn_duration == 0:
            player_input = None
            start_time = pygame.time.get_ticks()

            # Player has 3 seconds to input a key
            while pygame.time.get_ticks() - start_time < 3000:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            player_input = "a"
                        elif event.key == pygame.K_d:
                            player_input = "d"
                        elif event.key == pygame.K_w:
                            player_input = "w"
                        elif event.key == pygame.K_s:
                            player_input = "s"

            # Check if the player's input matches the enemy's pattern
            if player_input is not None:
                for enemy in enemies:
                    enemy_move = enemy.get_next_move(enemy_pattern_index)
                    if (
                        (player_input == "a" and enemy_move == "L")
                        or (player_input == "d" and enemy_move == "R")
                        or (player_input == "s" and enemy_move == "Both")
                        or (player_input == "w" and enemy_move == "Rest")
                    ):
                        print("Player successfully parried!")
                    else:
                        print("Player failed to parry. Player takes 1 point of damage.")
                        player_health -= 1

                enemy_pattern_index = (enemy_pattern_index + 1) % len(enemies[0].pattern)

        # Check for game over conditions
        if player_health <= 0 or enemy_health <= 0:
            # Draw the return button
            return_button = pygame.Rect(300, 400, 200, 50)
            pygame.draw.rect(screen, (0, 128, 255), return_button)
            font = pygame.font.Font(None, 36)
            text = font.render("Return to Welcome Screen", True, (255, 255, 255))
            screen.blit(text, (310, 415))

            # Check if the return button is clicked
            if return_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                welcome_screen = WelcomeScreen()
                choice = welcome_screen.run()
                if choice == "start":
                    # Restart the game
                    main_game(screen, clock, level=1)
                elif choice == "customize":
                    # Customize screen logic
                    pass

        pygame.display.flip()
        clock.tick(FPS)
        current_turn += 1

    pygame.quit()
    sys.exit()
