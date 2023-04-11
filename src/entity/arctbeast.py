import random
import pygame
from pygame import image, Rect
from pygame.math import Vector2

from src.lib.sprite import Sprite
from src.lib.transform import Transform
from src.entity.entity import Entity
from src.entity.crystal import Crystal

# Entity class for the arctbeast
class Boss(Entity):
    def __init__(self):
        super().__init__(
            Transform(Vector2(600,180), 0, 711, 364),
            Sprite(image.load('assets/sprites/arctbeast/arctbeast.png')),
        )
        self.rect = self.get(Transform).get_hitbox()
        self.get(Sprite).set_rect(self.get(Transform).pos)
        self.hp = 500

        # Variables for crystal shooting
        self.crystals = []
        self.cooldown = 0

        # Variables for invul animation
        self.hit = False
        self.invul = 0
        self.flicker = False

        # Sounds
        self.hit_sound = pygame.mixer.Sound("assets/sounds/effects/arctbeast_hit.wav")
        self.hit_sound.set_volume(0.05)

        self.death = pygame.mixer.Sound("assets/sounds/effects/arctbeast_death.wav")
        self.death.set_volume(0.05)

    def update(self):
        # Shoot crystals off cooldown
        if self.cooldown <= 0:
            self.shoot()
        else:
            self.cooldown -= 1

        # Update crystals
        for crystal in self.crystals:
            crystal.update()

            # If out of bounds, destroy the crystal
            if crystal.get(Transform).pos.y > 832 or crystal.get(Transform).pos.x < 0 or crystal.get(Transform).pos.x > 1216:
                if crystal in self.crystals:
                        self.crystals.remove(crystal)

            # If crystal hitting arctbeast after being reflected by a bullet
            if Rect.colliderect(self.rect, crystal.get(Transform).get_hitbox()):
                if crystal.direction.y < 0:
                    if self.invul <= 0:
                        self.hp -= 50
                        self.hit = True
                        self.invul = 200
                        if self.hp > 0: 
                            pygame.mixer.Sound.play(self.hit_sound)
                        else: 
                            pygame.mixer.Sound.play(self.death)
                    if crystal in self.crystals:
                        self.crystals.remove(crystal)

        # Update invincibility frames
        if self.invul > 0:
            self.invul -= 1        
        else:
             self.flicker = False    

        # If boss is in invul, flicker sprite a few times per second
        if self.invul > 0:
            if self.invul % 10 == 0:
                self.flicker = not self.flicker
             
    def shoot(self):
        # Create new crystal
        x = random.randint(260, 880)
        self.crystals.append(Crystal(x))

        # Start shooting cooldown
        self.cooldown = 25


    def render(self, screen):
        # Drawing the boss if not flickering
        if not self.flicker:
            sprite = self.get(Sprite)
            sprite.render(screen)
        
        # Drawing crystals
        for crystal in self.crystals:
             crystal.render(screen)

