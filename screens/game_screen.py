import pygame
import sys
import csv
from pygame.locals import *
from screens.welcome_screen import WelcomeScreen
from enemy import Enemy
from player import Player
from screens.customize_screen import CustomizeScreen
from screens.victory_screen import VictoryScreen
from screens.defeat_screen import DefeatScreen
from constants import *

# Constants
timer_interval = 3000
countdown_timer = timer_interval
player = Player()
# Define enemy names and load all enemies
enemy_names = ["Enemy1", "Enemy2", "Enemy3"]
enemies = [Enemy(name) for name in enemy_names]
enemy_counter = 0
#default enemy so the stupid function stops freaking out
enemy = enemies[0]
isAnimating = False
isReturning = False
ANIMATION_EVENT_LEFT = pygame.USEREVENT + 1
ANIMATION_EVENT_RIGHT = pygame.USEREVENT + 2
ANIMATION_EVENT_MIDDLE = pygame.USEREVENT + 3


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

def successful_parry(screen):
    success_text = font.render("PARRY!", True, (0, 0, 0))
    success_location = success_text.get_rect(center=(400, 500))
    screen.blit(success_text, success_location)
    pygame.display.flip()
    pygame.time.delay(1000)
    player_input = None

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

    # Load patterns from the csv file
    if level == 1:
        enemy = Enemy("Enemy1")
    elif level == 2:
        enemy = Enemy("Enemy2")
    elif level == 3:
        enemy = Enemy("Enemy3")
    elif level == 4:
        enemy = Enemy("CustomEnemy")

    enemy.load_pattern()
    
    enemy_pattern_index = 0

    font = pygame.font.Font(None, 36)

    # Draw the player and enemies at the beginning
    screen.fill(WHITE)
    screen.blit(player.image, player.rect)
    screen.blit(enemy.image, enemy.rect)
    pygame.display.flip()

    pygame.time.set_timer(ANIMATION_EVENT_MIDDLE, 3000)
    pygame.time.set_timer(ANIMATION_EVENT_LEFT, 3000)
    pygame.time.set_timer(ANIMATION_EVENT_RIGHT, 3000)

    while player.hp > 0:
        events = pygame.event.get()
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

        # animation handlers
        for event in events:
            if event.type == ANIMATION_EVENT_LEFT:
                enemy.left_attack()
                player.left_dodge()
                pygame.time.delay(1000)
                player.return_position()
                isAnimating = False
            elif event.type == ANIMATION_EVENT_RIGHT:
                enemy.left_attack() # testing animation, will make right_attack later
                player.right_dodge()
                isAnimating = False
            elif event.type == ANIMATION_EVENT_MIDDLE:
                enemy.left_attack()
                player.left_dodge()
                isAnimating = False

        for event in events:
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
        
        for event in events:
            if event.type == pygame.USEREVENT:
                enemy_move = enemy.get_next_move(enemy_pattern_index)
                enemy_pattern_index = (enemy_pattern_index + 1) % len(enemy.pattern)

                if player_input == "a" and enemy_move == "L":
                    successful_parry(screen)
                    pygame.event.post(pygame.event.Event(ANIMATION_EVENT_LEFT))
                elif player_input == "d" and enemy_move == "R":
                    successful_parry(screen)
                    pygame.event.post(pygame.event.Event(ANIMATION_EVENT_RIGHT))
                elif player_input == "s" and enemy_move == "Both":
                    successful_parry(screen)
                    pygame.event.post(pygame.event.Event(ANIMATION_EVENT_MIDDLE))
                elif (
                    (player_input == "a" and enemy_move == "Rest") or
                    (player_input == "d" and enemy_move == "Rest") or
                    (player_input == "s" and enemy_move == "Rest")
                    ):
                    display_message(screen, "Enemy Heals 1 HP", 30, 1000)
                    enemy.hp += 1
                elif (player_input == "w" and enemy_move == "Rest"):
                    display_message(screen, "Player attacked the enemy!", 30, 1000)
                    enemy.hp -= 1
                else:
                    display_message(screen, "Player got hit!", 30, 1000)
                    player.hp -= 1

                player_input = None
                start_time = pygame.time.get_ticks()

        remaining_time = max(0, timer_interval - (pygame.time.get_ticks() - start_time))

        ctimer = font.render(f"Countdown: {remaining_time // 1000} seconds", True, (0,0,0))
        screen.blit(ctimer, (30, 30))

        # Check for game over conditions
        if player.hp == 0:
            return player.hp
        if enemy.hp == 0:
            return enemy.hp

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    # Add any additional initialization or calls here if needed
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    main_game(screen, clock)
