# game_screen.py
import pygame
import sys
import toml
from pygame.locals import *
from screens.welcome_screen import WelcomeScreen
from enemy import Enemy
from player import Player
from screens.customize_screen import CustomizeScreen

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

    if level == 1:
        enemy = enemies[0]
    elif level == 2:
        enemy = enemies[1]
    elif level == 3:
        enemy = enemies[2]
    elif custom_pattern is not None:
        enemy = enemies[3]

    enemy.load_pattern(patterns)
    print(f"Loading patterns for {enemy.name}")
    print(f"Loaded patterns: {enemy.pattern}")
    # Global variables and constants
    turn_duration = 3000  # 3 seconds in milliseconds
    enemy_pattern_index = 0

    # Create font for textboxes
    font = pygame.font.Font(None, 36)

    # Draw the player and enemies at the beginning
    screen.fill(WHITE)
    screen.blit(player.image, player.rect)
    screen.blit(enemy.image, enemy.rect)
    pygame.display.flip()

    # Wait for a short moment (e.g., 1 second) to display the initial setup
    pygame.time.delay(1000)

    parry_start_time = 0
    successful_parry = False

    while player_health > 0:
        screen.fill(WHITE)

        # Draw the player
        screen.blit(player.image, player.rect)

        # Draw the enemies
        screen.blit(enemy.image, enemy.rect)

        # Display player health in the upper left corner
        player_health_text = font.render(f"Player Health: {player_health}", True, (0, 0, 0))
        screen.blit(player_health_text, (10, 10))

        # Display enemy health in the upper right corner
        enemy_health_text = font.render(f"Enemy Health: {enemy_health}", True, (0, 0, 0))
        screen.blit(enemy_health_text, (600, 10))

        # Display current enemy move in the center, above the enemy
        enemy_move_text = font.render(f"Enemy Move: {enemy.get_next_move(enemy_pattern_index)}", True, (0, 0, 0))
        text_rect = enemy_move_text.get_rect(center=(400, 50))
        screen.blit(enemy_move_text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check if it's the player's turn
        player_input = None
        start_time = pygame.time.get_ticks()

        # Player has 3 seconds to input a key
        while pygame.time.get_ticks() - start_time < 1000:
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
            enemy_move = enemy.get_next_move(enemy_pattern_index)
            if (
                (player_input == "a" and enemy_move == "L")
                or (player_input == "d" and enemy_move == "R")
                or (player_input == "s" and enemy_move == "Both")
            ):
                successful_parry = True
                parry_start_time = pygame.time.get_ticks()
                print("Player successfully parried!")
            elif (player_input == "w" and enemy_move == "Rest"):
                print("Player successfully attacked!")
                enemy_health -= 1
            else:
                print("Player failed to parry. Player takes 1 point of damage.")
                player_health -= 1

            enemy_pattern_index = (enemy_pattern_index + 1)

        if successful_parry:
            display_message(screen, "Player successfully parried!", 30, 1000)
            successful_parry = False

        if enemy_health == 0:
            display_message(screen, "Player wins!", 30, 1000)

            # Draw the restart button
            restart_button = pygame.Rect(300, 400, 200, 50)
            pygame.draw.rect(screen, (0, 128, 0), restart_button)
            restart_text = font.render("Next Enemy", True, (255, 255, 255))
            screen.blit(restart_text, (340, 415))

            # Check if the restart button is clicked
            if restart_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                level += 1  # Move to the next enemy
                enemy_health = 3  # Reset enemy health
                enemy_pattern_index = 0  # Reset enemy pattern index
                current_turn = 0  # Reset the turn count
                successful_parry = False  # Reset successful parry flag
                main_game(screen, clock, level=level)

        # Check for game over conditions
        if player_health == 0:
            # Draw the return button
            return_button = pygame.Rect(300, 400, 200, 50)
            pygame.draw.rect(screen, (0, 128, 255), return_button)
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
                    customize_screen = CustomizeScreen()
                    customize_screen.run()
                    pass

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # Add any additional initialization or calls here if needed
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    main_game(screen, clock)
