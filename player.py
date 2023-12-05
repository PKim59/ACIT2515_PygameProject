# player.py
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))  # Blue color for the player
        self.rect = self.image.get_rect()
        self.rect.center = (400, 500)  # Initial position at the bottom middle
        self.hp = 3

    def update(self):
        pass  # You can add any updates needed for the player


