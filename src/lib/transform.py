import pygame.draw as draw
import pygame
from pygame.math import Vector2

# Class to manage object size, position, and rotations
class Transform:
    def __init__(self, pos: Vector2, angle: float, width: int, height: int):
        self.pos: Vector2 = pos
        self.angle: float = angle
        self.width: int = width
        self.height: int = height

    # Debug to draw hitboxes of each character (in case some sprites are not fully square)
    def draw_debug(self, screen):
        draw.rect(screen, (255, 0, 0), (self.pos.x - self.width / 2, self.pos.y - self.height / 2, self.width, self.height), 1)
        draw.line(screen, (0, 255, 0), (self.pos.x, self.pos.y), self.pos + Vector2(10, 0).rotate(-self.angle), 1)

    # Returns the square hitbox of the entity (regardless of rotation) by using the entity's rectangular position and dimensions 
    def get_hitbox(self):
        return pygame.Rect(self.pos.x - self.width / 2, self.pos.y - self.height / 2, self.width, self.height)
