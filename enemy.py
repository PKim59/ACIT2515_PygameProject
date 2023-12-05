import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.pattern = []
        self.hp = 3

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

    def load_pattern(self, patterns):
        loaded_pattern = patterns.get(self.name, {}).get('pattern', [])
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

    def update(self):
        pass  # You can add any updates needed for the enemy sprite
