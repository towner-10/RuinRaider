from pygame import Surface
from pygame.math import Vector2
from pygame import image
import pygame.transform as transform

# Class to handle sprite objects
class Sprite:
    def __init__(self, sprite: Surface):
        self.sprite = sprite
        self.original_sprite = self.sprite

    # Set rect
    def set_rect(self, pos):
        self.rect = self.sprite.get_rect(center=(pos[0], pos[1]))

    # Rotate the sprite
    def rotate(self, angle):
        self.sprite = transform.rotate(self.original_sprite, angle)
        self.rect = self.sprite.get_rect(center=self.rect.center)

    # Move the sprite
    def move(self, vector: Vector2):
        self.rect.center = vector

    # Resize the sprite
    def scale(self, width, height):
        self.sprite = transform.scale(self.sprite, (width, height))
    
    # Update the sprite
    def set_sprite(self, img_path):
        self.sprite = image.load(img_path)
        self.original_sprite = self.sprite

    # Draw the sprite to the screen
    def render(self, screen: Surface):
        screen.blit(self.sprite, self.rect)
