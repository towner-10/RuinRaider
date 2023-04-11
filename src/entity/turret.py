import pygame
from pygame import image
from pygame.math import Vector2

import src.inventory.item as item

from src.lib.transform import Transform
from src.lib.sprite import Sprite
from src.entity.character import Character

# Turret class
class Turret(Character):
    def __init__(self, position: Vector2 = Vector2(0,0), direction:Vector2 = Vector2(0,0)):
        super().__init__(image.load('assets/sprites/turret.png'), position, 270)
        self.damage = 40
        self.position = position
        self.cooldown = 0
        self.fire_rate = 1
        self.bullets = []
        self.damage_player = False
        self.direction = direction

    # Method to spawn bullets
    def shoot(self, pos: Vector2, angle: float):
        
        # Create new bullet
        new_bullet = item.Bullet(Vector2.copy(self.direction), 8, Transform(pos, angle, 16, 16), "assets/sprites/items/arctium_bullet.png")
        # Resizing bullet sprite
        new_bullet.get(Sprite).scale(16, 16)
        new_bullet.get(Sprite).set_rect(new_bullet.get(Transform).pos)

        self.bullets.append(new_bullet)

        # Start shooting cooldown
        self.cooldown = 39

    # Method to update bullets
    def update_bullets(self, barriers, player):
        # Tracking bullet collisions (remove bullets upon collision with objects)
        for bullet in self.bullets:
            bullet.update()

            # If collided with the player, deal damage
            if pygame.Rect.colliderect(bullet.get(Transform).get_hitbox(), player.get_hitbox()):
                # Prevent fatal error when bullet is removed twice
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
                    self.damage_player = True
                break

            # If collided with a wall, destroy the bullet
            for barrier in barriers:
                if pygame.Rect.colliderect(bullet.get(Transform).get_hitbox(), barrier):
                    # Prevent fatal error when bullet is removed twice
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break

    # Update fire rate
    def update_fire_rate(self):
        if self.cooldown > 0:
            self.cooldown -= self.fire_rate

    def update(self, player):
        self.update_fire_rate()
        self.damage_player = False # Reset damage flag

        # Turret shoots during predefined intervals, creating an obstacle of bullets
        if self.cooldown <= 0:
            self.shoot(Vector2.copy(self.get(Transform).pos), self.get(Transform).angle)

    def render(self, screen):
        # Rotate in direction of movement
        self.rotate(-self.direction.as_polar()[1])

        # Render in screen
        super().render(screen)

        self.render_bullets(screen)

    # Method to draw bullets
    def render_bullets(self, screen):
        for bullet in self.bullets:
            bullet.render(screen)