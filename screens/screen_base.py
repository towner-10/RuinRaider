import pygame

# Base class for all screens in the game
# includes all necessary methods and allows for seamless transitions between screens
class ScreenBase:
    def __init__(self):
        self.next = self

    def process_input(self, events: list):
        pass

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        pass

    def switch_to_scene(self, next_scene: "ScreenBase"):
        self.next = next_scene

    def terminate(self):
        self.switch_to_scene(None)
