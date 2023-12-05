from screens.screen_base import ScreenBase
from pygame.locals import *
import pygame

class VictoryScreen(ScreenBase):
    def __init__(self):
        super().__init__()

    def display(self):
        running = True
        while running:
            self.handle_events()

            # Implementation of victory screen
            self.screen.fill((255, 255, 255))  # Clear the screen (replace with your background)
            
            # Draw victory message
            victory_text = self.font.render("Player wins!", True, (0, 0, 0))
            self.screen.blit(victory_text, (300, 200))

            # Draw the restart button
            restart_button = pygame.Rect(300, 400, 200, 50)
            pygame.draw.rect(self.screen, (0, 128, 0), restart_button)
            restart_text = self.font.render("Next Enemy", True, (255, 255, 255))
            self.screen.blit(restart_text, (340, 415))

            self.update_display()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if restart_button.collidepoint(event.pos):
                        running = False  # Exit the loop

        return True  # Signal to move to the next level
