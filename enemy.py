# enemy.py
import yaml

class Enemy:
    def __init__(self, name):
        self.name = name
        self.pattern = []

    def load_pattern(self, patterns):
        self.pattern = patterns.get(self.name, [])

    def get_next_move(self, current_index):
        return self.pattern[current_index % len(self.pattern)]
