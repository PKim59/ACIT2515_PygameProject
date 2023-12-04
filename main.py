# main.py
import pygame
import sys
import yaml
from screens.welcome_screen import WelcomeScreen
from screens.customize_screen import CustomizeScreen
from enemy import Enemy

# Load patterns from the TOML file
with open("patterns.toml", "r") as file:
    patterns = yaml.load(file, Loader=yaml.FullLoader)

# Initialize player and enemy health
player_health = 3
enemy_health = 3

# Define enemy names
enemy_names = ["Enemy1", "Enemy2", "Enemy3"]

# Create Enemy instances and load patterns
enemies = [Enemy(name) for name in enemy_names]
for enemy in enemies:
    enemy.load_pattern(patterns)

# Global variables and constants
current_turn = 0
turn_duration = 3000  # 3 seconds in milliseconds
FPS = 60

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Create Pygame screen and sprite groups
screen = pygame.display.set_mode((800, 600))
all_sprites = pygame.sprite.Group()

# Main Game Loop
def main_game():
    global current_turn, patterns, enemies, all_sprites, screen, clock, FPS, player_health, enemy_health

    player_input = None
    enemy_pattern_index = 0

    # Game loop
    running = True
    while running:
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
        if player_health <= 0:
            print("Game Over - Player has no health.")
            running = False
        elif all(enemy_health <= 0 for enemy_health in [enemy_health for enemy in enemies]):
            print("Game Over - All enemies defeated!")
            running = False

        # Update
        all_sprites.update()

        # Draw
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)

        # Increment turn counter
        current_turn += 1

        pygame.display.flip()
        clock.tick(FPS)

# Main Program
while True:
    welcome_screen = WelcomeScreen()
    choice = welcome_screen.run()

    if choice == "start":
        # Start the game
        main_game()
    elif choice == "customize":
        customize_screen = CustomizeScreen()
        customize_screen.run()
