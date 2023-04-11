import pygame
import math
from pygame.math import Vector2
from pygame import Surface

import src.lighting.lighting as lighting
from src.lib.transform import Transform
from src.lib.sprite import Sprite
from src.entity.entity import Entity
from src.entity.arctbeast import Boss

# Parent Item class
class Item():
    def __init__(self, x, y, img_path):
        self.img_path = img_path
        self.image = pygame.image.load(self.img_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x, y)
        self.collected = False

    def get_rect(self):
        return self.rect
    
    def set_light(self, light: lighting.Light):
        self.__light = light
    
    def get_light(self) -> lighting.Light:
        return self.__light

    def render(self, screen: pygame.Surface):
        screen.blit(self.image, (self.x, self.y))

# Class to manage weapon properties (extends Item)
class Weapon(Item):
    def __init__(self, x = 0, y = 0, img_path = "assets\sprites\empty_image.png", damage = 0, fire_rate = 0):
        super().__init__(x, y, img_path)
        self.damage = damage
        self.fire_rate = fire_rate

        # Variables to manage cooldown and bullet firing
        self.cooldown = 0
        self.bullets = []
        self.shooting = False

        # Tracking arctium blaster (who has stronger bullets)
        self.is_arctium = False

        # Sound effects
        self.enemy_hit_sound = pygame.mixer.Sound("assets/sounds/effects/enemy_hit.wav")
        self.enemy_hit_sound.set_volume(0.3)

        self.crystal_sound = pygame.mixer.Sound("assets/sounds/effects/crystal_hit.wav")
        self.crystal_sound.set_volume(0.3)

    # Method to spawn bullets
    def shoot(self, pos:Vector2, angle: float):
        self.shooting = True
        # Calculate the normalized direction vector
        direction = Vector2(math.cos(math.radians(-angle)), math.sin(math.radians(-angle)))

        # Create new bullet
        new_bullet = Bullet(direction, 20, Transform(pos, angle, 16, 16), "assets/sprites/items/bullet.png")
        self.bullets.append(new_bullet)

        # Start shooting cooldown
        self.cooldown = 15

    # Method to update bullets
    def update_bullets(self, barriers, enemies):
        self.update_fire_rate()

        # Tracking bullet collisions (remove bullets upon collision with objects)
        for bullet in self.bullets:
            bullet.update()

            # If collided with a wall, destroy the bullet
            for barrier in barriers:
                if pygame.Rect.colliderect(bullet.get(Transform).get_hitbox(), barrier):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break

            # If collided with an enemy, deal damage and destroy non-arctium bullets
            for enemy in enemies:
                if pygame.Rect.colliderect(bullet.get(Transform).get_hitbox(), enemy.get_hitbox()):
                    if bullet in self.bullets and not self.is_arctium:
                        self.bullets.remove(bullet)
                    enemy.hit(self.damage)
                    pygame.mixer.Sound.play(self.enemy_hit_sound)
                    break

    # Method to update bullets in boss level
    def update_boss(self, boss:Boss):
        self.update_fire_rate()

        # Tracking bullet collisions (remove bullets upon collision with objects)
        for bullet in self.bullets:
            bullet.update()

            # If out of bounds, destroy the bullet
            if bullet.get(Transform).pos.x < 0 or bullet.get(Transform).pos.x > 1216 or bullet.get(Transform).pos.y < 0 or bullet.get(Transform).pos.y > 832:
                if bullet in self.bullets:
                        self.bullets.remove(bullet)

            # If collided with crystal, destroy bullet and call method
            for crystal in boss.crystals:
                if pygame.Rect.colliderect(bullet.get(Transform).get_hitbox(), crystal.get(Transform).get_hitbox()):
                    crystal.direction = bullet.direction
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    pygame.mixer.Sound.play(self.crystal_sound)
                    break

    # Update fire rate
    def update_fire_rate(self):
        if self.cooldown > 0:
            self.cooldown -= self.fire_rate
        else:
            self.shooting = False                

    # Method to draw bullets
    def render_bullets(self, screen):
        for bullet in self.bullets:
            bullet.render(screen)

# Class to manage bullet objects
class Bullet(Entity):
    def __init__(self, direction: Vector2, speed: int, transform: Transform, img_path:str=""):
        super().__init__(Sprite(pygame.image.load(img_path)), transform)
        self.direction = direction
        self.speed = speed

    def render(self, screen: Surface):
        # Rotate in direction of movement
        self.get(Sprite).set_rect(self.get(Transform).pos)
        self.get(Sprite).rotate(-self.direction.as_polar()[1])

        # Render to screen
        self.get(Sprite).render(screen)

    # Move bullet in its direction
    def update(self):
        self.get(Transform).pos += self.direction * self.speed