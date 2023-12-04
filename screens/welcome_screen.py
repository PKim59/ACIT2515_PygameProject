# screens/welcome_screen.py
from screens.screen_base import ScreenBase
import pygame

class WelcomeScreen(ScreenBase):
    def __init__(self):
        super().__init__()
        self.start_button = pygame.Rect(350, 200, 100, 50)
        self.customize_button = pygame.Rect(350, 300, 100, 50)
        self.quit_button = pygame.Rect(350, 400, 100, 50)

    def run(self):
        run_condition = True
        while run_condition:
            self.handle_events()
            self.screen.fill((255, 255, 255))
            title_text = self.font.render("Fighting Time", True, (0, 0, 0))
            self.screen.blit(title_text, (250, 50))

            pygame.draw.rect(self.screen, (0, 0, 255), self.start_button)
            pygame.draw.rect(self.screen, (0, 0, 255), self.customize_button)
            pygame.draw.rect(self.screen, (0, 0, 255), self.quit_button)

            start_text = self.font.render("Start", True, (255, 255, 255))
            customize_text = self.font.render("Customize", True, (255, 255, 255))
            quit_text = self.font.render("Quit", True, (255, 255, 255))

            self.screen.blit(start_text, (self.start_button.centerx - start_text.get_width() // 2, self.start_button.centery - start_text.get_height() // 2))
            self.screen.blit(customize_text, (self.customize_button.centerx - customize_text.get_width() // 2, self.customize_button.centery - customize_text.get_height() // 2))
            self.screen.blit(quit_text, (self.quit_button.centerx - quit_text.get_width() // 2, self.quit_button.centery - quit_text.get_height() // 2))

            self.update_display()

            if hasattr(self, 'choice'):
                return self.choice

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.collidepoint(event.pos):
                    self.choice = "start"
                    return self.choice
                elif self.customize_button.collidepoint(event.pos):
                    self.choice = "customize"
                    return self.choice
                elif self.quit_button.collidepoint(event.pos):
                    pygame.quit()

