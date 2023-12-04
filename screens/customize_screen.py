# customize_screen.py
import pygame
import sys
import toml


class CustomizeScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.pattern = []
        self.font = pygame.font.Font(None, 36)
        self.textbox = pygame.Rect(50, 450, 700, 50)
        self.text_color = pygame.Color('black')
        self.text = ''

        # Check for existing "CustomEnemy" pattern in the TOML file
        try:
            with open("patterns.toml", "r") as file:
                patterns = toml.load(file)
                self.pattern = patterns.get("CustomEnemy", [])
                self.update_text()
        except FileNotFoundError:
            pass

        # Button positions and dimensions
        button_positions = [
            (50, 100, 100, 50, "Left"),
            (200, 100, 100, 50, "Right"),
            (350, 100, 100, 50, "Both"),
            (500, 100, 100, 50, "Rest"),
            (200, 200, 150, 50, "Remove Last"),
            (400, 200, 100, 50, "Clear"),
            (200, 300, 150, 50, "Save and Load"),
            (400, 300, 100, 50, "Start Custom Fight"),  # New button
            (600, 300, 100, 50, "Back")
        ]

        # Create buttons as Rect objects
        self.buttons = [pygame.Rect(x, y, width, height) for x, y, width, height, label in button_positions]
        self.button_labels = [label for x, y, width, height, label in button_positions]

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_button_click(event.pos)

            self.screen.fill((255, 255, 255))

            # Draw buttons
            for button, label in zip(self.buttons, self.button_labels):
                pygame.draw.rect(self.screen, (200, 200, 200), button)
                text_surface = self.font.render(label, True, self.text_color)
                button_center = button.x + button.width // 2 - text_surface.get_width() // 2, button.y + 10
                self.screen.blit(text_surface, button_center)

            # Draw ongoing custom pattern textbox
            pygame.draw.rect(self.screen, (200, 200, 200), self.textbox)
            text_surface = self.font.render(self.text, True, self.text_color)
            self.screen.blit(text_surface, (self.textbox.x + 10, self.textbox.y + 10))

            pygame.display.flip()
            self.clock.tick(60)

    def handle_button_click(self, pos):
        for button, label in zip(self.buttons, self.button_labels):
            if button.collidepoint(pos):
                if label == "Remove Last":
                    self.remove_last_move()
                elif label == "Clear":
                    self.clear_pattern()
                elif label == "Save and Load":
                    self.save_and_load()
                elif label == "Start Custom Fight":
                    self.start_custom_fight()
                elif label == "Back":
                    self.back()
                else:
                    self.add_move(label)

    def add_move(self, move):
        self.pattern.append(move)
        self.update_text()

    def remove_last_move(self):
        if self.pattern:
            self.pattern.pop()
            self.update_text()

    def clear_pattern(self):
        self.pattern = []
        self.update_text()

    def update_text(self):
        self.text = ', '.join(self.pattern)

    def save_and_load(self):
        # Save the custom pattern to the patterns dictionary
        with open("patterns.toml", "r") as file:
            patterns = toml.load(file)

        patterns["CustomEnemy"] = self.pattern  # Use the correct key
        with open("patterns.toml", "w") as file:
            toml.dump(patterns, file)

    def start_custom_fight(self):
        # Save the custom pattern to the patterns dictionary
        with open("patterns.toml", "r") as file:
            patterns = toml.load(file)

        patterns["CustomEnemy"] = self.pattern  # Use the correct key
        with open("patterns.toml", "w") as file:
            toml.dump(patterns, file)

        # Exit the customization screen and start the game
        from main import main_game
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        main_game(screen, clock, level=4)

    def back(self):
        # Exit the customization screen
        pygame.quit()
        sys.exit()
