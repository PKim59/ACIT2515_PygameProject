import pygame
import csv

class Enemy(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.pattern = []
        self.hp = 3
        self.isAnimating = False
        self.isReturning = False

        # Set color based on enemy name
        if self.name == "Enemy1":
            color = (255, 0, 0)  # Red
        elif self.name == "Enemy2":
            color = (0, 0, 255)  # Blue
        elif self.name == "Enemy3":
            color = (255, 255, 0)  # Yellow
        else:
            color = (0, 0, 0)  # Default color (white)

        # Sprite-related code
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)  # Initial position at the center

    def load_pattern(self):
        with open("patterns.csv", "r") as file:
            reader = csv.reader(file)
            patterns = {rows[0]: rows[1:] for rows in reader}

        loaded_pattern = patterns.get(self.name, [])
        print(f"Loading patterns for {self.name}")
        print(f"Loaded patterns: {loaded_pattern}")
        self.pattern = loaded_pattern

    def get_next_move(self, current_index):
            if not self.pattern:
                return None  # Handle empty pattern gracefully
            try:
                return self.pattern[current_index % len(self.pattern)]
            except Exception as e:
                print(f"Error in get_next_move: {e}")
                print(f"Name: {self.name}, Pattern: {self.pattern}, Index: {current_index}")

    def return_position(self):
        self.rect.center = (400, 300)
        pass  # You can add any updates needed for the enemy sprite

    def left_attack(self):
        # Define the start, midpoint, and end points
        start_pos = pygame.Vector2(400, 300)
        mid_pos = pygame.Vector2(300, 500)
        end_pos = start_pos

        # Define the speed of the animation
        speed = 0.05

        # Calculate the direction vector
        if not self.isReturning:
            direction = (mid_pos - self.rect.center).normalize()
        else:
            direction = (end_pos - self.rect.center).normalize()

        # Update the position
        self.rect.center += direction * speed

        # If the cube has reached the midpoint and is not returning, start returning
        if (self.rect.center - mid_pos).length() < speed and not self.isReturning:
            self.isReturning = True

        # If the cube has reached the end position and is returning, stop the animation
        if (self.rect.center - end_pos).length() < speed and self.isReturning:
            self.isAnimating = False
            self.isReturning = False