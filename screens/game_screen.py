import pygame
import sys
import toml
from pygame.locals import *
from screens.welcome_screen import WelcomeScreen
from enemy import Enemy
from player import Player
from screens.customize_screen import CustomizeScreen
from screens.victory_screen import VictoryScreen
from screens.defeat_screen import DefeatScreen

# Constants
FPS = 60
WHITE = (255, 255, 255)
timer_interval = 3000
countdown_timer = timer_interval
start_time = pygame.time.get_ticks()
player = Player()
# Define enemy names and load all enemies
enemy_names = ["Enemy1", "Enemy2", "Enemy3"]
enemies = [Enemy(name) for name in enemy_names]
enemy_counter = 0
#default enemy so the stupid function stops freaking out
enemy = enemies[0]
isAnimating = False
isReturning = False

original_player_pos = player.rect.x, player.rect.y 
original_enemy_pos = enemy.rect.x, enemy.rect.y

# Initialize Pygame
pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 3000)  # 2000 milliseconds = 2 seconds

def display_message(screen, message, font_size, duration):
    font = pygame.font.Font(None, font_size)
    text = font.render(message, True, (0, 0, 0))
    rect = text.get_rect(center=(400, 300))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.delay(duration)

def update_positions():
    player.rect.x = 450
    player.rect.y = 450
    enemy.rect.x = 440
    enemy.rect.y = 440
    pygame.display.flip()


def return_positions():
    player.rect.x = original_player_pos[0]
    player.rect.y = original_player_pos[1]
    enemy.rect.x = original_enemy_pos[0]
    enemy.rect.y = original_enemy_pos[1]
    pygame.display.flip()

def main_game(screen, clock, level=1, custom_pattern=None):
    player = Player()
    start_time = pygame.time.get_ticks()
    player_input = None
    isAnimating = False

    # Load patterns from the TOML file
    with open("patterns.toml", "r") as file:
        patterns = toml.load(file)
    enemy_counter = 0
    if level == 1:
        enemy = enemies[enemy_counter]
    elif level == 2:
        enemy = enemies[enemy_counter + 1]
    elif level == 3:
        enemy = enemies[enemy_counter + 2]
    elif custom_pattern is not None:
        enemy = enemies[3]

    original_player_pos = (player.rect.x, player.rect.y)
    original_enemy_pos = (enemy.rect.x, enemy.rect.y)
    
    enemy.load_pattern(patterns)
    # print(f"Loading patterns for {enemy.name}")
    # print(f"Loaded patterns: {enemy.pattern}")
    
    enemy_pattern_index = 0

    font = pygame.font.Font(None, 36)
    successful_parry = False

    # Draw the player and enemies at the beginning
    screen.fill(WHITE)
    screen.blit(player.image, player.rect)
    screen.blit(enemy.image, enemy.rect)
    pygame.display.flip()

    while player.hp > 0:
        screen.fill(WHITE)

        # Draw the player
        screen.blit(player.image, player.rect)

        # Draw the enemy
        screen.blit(enemy.image, enemy.rect)

        # Display player health in the upper left corner
        player_health_text = font.render(f"Player Health: {player.hp}", True, (0, 0, 0))
        screen.blit(player_health_text, (10, 10))

        # Display enemy health in the upper right corner
        enemy_health_text = font.render(f"Enemy Health: {enemy.hp}", True, (0, 0, 0))
        screen.blit(enemy_health_text, (600, 10))

        # Display current enemy move in the center, above the enemy
        enemy_move_text = font.render(f"Enemy Move: {enemy.get_next_move(enemy_pattern_index)}", True, (0, 0, 0))
        text_rect = enemy_move_text.get_rect(center=(400, 50))
        screen.blit(enemy_move_text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
            # timer event cycle code: remember any gameplay triggers occur here.
            elif event.type == pygame.USEREVENT:
                enemy.load_pattern(patterns)
                enemy_move = enemy.get_next_move(enemy_pattern_index)
                if (
                    (player_input == "a" and enemy_move == "L")
                    or (player_input == "d" and enemy_move == "R")
                    or (player_input == "s" and enemy_move == "Both")
                ):
                    update_positions()
                    success_text = font.render("PARRY!", True, (0, 0, 0))
                    success_location = success_text.get_rect(center=(400, 500))
                    screen.blit(success_text, success_location)
                    pygame.display.flip()
                    pygame.time.delay(1000)
                    return_positions()
                    player_input = None
                elif (
                    (player_input == "a" and enemy_move == "Rest") or
                    (player_input == "d" and enemy_move == "Rest") or
                    (player_input == "s" and enemy_move == "Rest")
                    ):
                    display_message(screen, "Enemy Heals 1 HP", 30, 1000)
                    enemy.hp += 1
                    player_input = None
                elif (player_input == "w" and enemy_move == "Rest"):
                    display_message(screen, "Player attacked the enemy!", 30, 1000)
                    enemy.hp -= 1
                    player_input = None                    
                else:
                    display_message(screen, "Player got hit!", 30, 1000)
                    player.hp -= 1
                    player_input = None
                # print(enemy_pattern_index)
                # print(enemy.get_next_move(enemy_pattern_index))
                # print(enemies)
                enemy_pattern_index = (enemy_pattern_index + 1)
                start_time = pygame.time.get_ticks()

        remaining_time = max(0, timer_interval - (pygame.time.get_ticks() - start_time))

        ctimer = font.render(f"Countdown: {remaining_time // 1000} seconds", True, (0,0,0))
        screen.blit(ctimer, (30, 30))
        pygame.display.flip()

        if enemy.hp == 0:
            victory_screen = VictoryScreen()
            if victory_screen.display():
                level += 1
                if enemy_counter > len(enemies):
                    enemy_counter = 0
                else:
                    enemy = enemies[enemy_counter + 1]
                enemy.hp = 3 
                enemy_pattern_index = 0
                pygame.display.flip()

        # Check for game over conditions
        if player.hp == 0:
            defeat_screen = DefeatScreen()
            if defeat_screen.display():
                welcome_screen = WelcomeScreen()
                choice = welcome_screen.run()
                if choice == "start":
                    # Restart the game
                    main_game(screen, clock, level=1)
                elif choice == "customize":
                    #go to customize screen
                    customize_screen = CustomizeScreen()
                    customize_screen.run()
                    pass

        pygame.display.flip()
        clock.tick(FPS)

    return player.hp
    # pygame.quit()
    # sys.exit()

if __name__ == "__main__":
    # Add any additional initialization or calls here if needed
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    main_game(screen, clock)
