import json
import pygame
import math

from pygame.math import Vector2

import src.inventory.inventory_manager as inventory
import src.ui.ui_elements as ui_elements

from src.lib.transform import Transform
from src.lib.sprite import Sprite
from src.entity.character import Character
from src.inventory.item import Weapon
from src.entity.arctbeast import Boss

# Class for the main player, including most interactions
class Player(Character):
    def __init__(self, spriteSet=["assets\sprites\empty_image.png","",""], position=Vector2(0,0), angle=0, pistol: Weapon = None, merc_pistol: Weapon = None, arct_blaster: Weapon = None):
        super().__init__(pygame.image.load(spriteSet[0]), position, angle)
        # Player stats
        self.currentHP = 100
        self.maxHP = 100
        self.kills = 0
        self.spriteSet = spriteSet

        # Movement variables
        self.direction = Vector2(0,0)
        self.moving = False
        self.base_speed = 2
        self.speed = self.base_speed
        self.webbed = False
        
        # Inventory weapons
        self.pistol = pistol
        self.merc_pistol = merc_pistol
        self.arct_blaster = arct_blaster
        
        # Invulnerability tracker
        self.invul = 0
        self.flicker = False

        # Player item/environment interaction sound effects
        self.pistol_sound = pygame.mixer.Sound("assets/sounds/effects/gunshot.wav")
        self.pistol_sound.set_volume(0.3)

        self.merc_pistol_sound = pygame.mixer.Sound("assets/sounds/effects/heavygun.wav")
        self.merc_pistol_sound.set_volume(0.3)

        self.arct_blaster_sound = pygame.mixer.Sound("assets/sounds/effects/revolver.wav")
        self.arct_blaster_sound.set_volume(0.3)

        self.heal_sound = pygame.mixer.Sound("assets/sounds/effects/maximize_008.ogg")
        self.heal_sound.set_volume(0.3)

        self.craft_sound = pygame.mixer.Sound("assets/sounds/effects/handleCoins.ogg")
        self.craft_sound.set_volume(0.3)

        self.empty_sound = pygame.mixer.Sound("assets/sounds/effects/handleCoins2.ogg")
        self.empty_sound.set_volume(0.3)

        self.damage_sound = pygame.mixer.Sound("assets/sounds/effects/hit.wav")
        self.damage_sound.set_volume(0.3)

        self.turret_sound = pygame.mixer.Sound("assets/sounds/effects/turret.wav")
        self.turret_sound.set_volume(0.3)

    # Processing player inputs 
    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Update moving variable for sprites
                if event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_a or event.key == pygame.K_d:
                    self.moving = True
                
                # Process WASD Inputs
                if event.key == pygame.K_w:
                    self.direction.y = -self.speed
                if event.key == pygame.K_s:
                    self.direction.y = self.speed
                if event.key == pygame.K_a:
                    self.direction.x = -self.speed
                if event.key == pygame.K_d:
                    self.direction.x = self.speed
            
            if event.type == pygame.KEYUP:
                # Processing keylifts for movement keys
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    self.direction.y = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    self.direction.x = 0

            # Shoot pistol if selected and clicked
            # NOTE: a pistol will not be shot if the player has no ammo
            if inventory.InventoryManager.getInstance().is_used(1, events):
                if self.pistol.cooldown <= 0 and inventory.InventoryManager.getInstance().get_count(4) > 0:
                    # Shoot pistol
                    pygame.mixer.Sound.play(self.pistol_sound)
                    self.pistol.shoot(Vector2.copy(self.get(Transform).pos), self.get(Transform).angle)
                    inventory.InventoryManager.getInstance().ammo_count -= 1
                elif self.pistol.cooldown <= 0:
                    pygame.mixer.Sound.play(self.empty_sound)

            # Shoot mercenary pistol if selected and clicked
            # NOTE: a mercenary pistol will not be shot if the player has no ammo
            if inventory.InventoryManager.getInstance().is_used(2, events):
                if self.merc_pistol.cooldown <= 0 and inventory.InventoryManager.getInstance().get_count(4) - 5 >= 0:
                    # Shoot mercenary pistol
                    pygame.mixer.Sound.play(self.merc_pistol_sound)
                    self.merc_pistol.shoot(Vector2.copy(self.get(Transform).pos), self.get(Transform).angle)
                    inventory.InventoryManager.getInstance().ammo_count -= 5
                elif self.merc_pistol.cooldown <= 0:
                    pygame.mixer.Sound.play(self.empty_sound)

            # Shoot arctium blaster if selected and clicked
            # NOTE: an arctium blaster will not be shot if the player has no Arctium crystals
            if inventory.InventoryManager.getInstance().is_used(3, events):
                if self.arct_blaster.cooldown <= 0 and inventory.InventoryManager.getInstance().get_count(6) > 0:
                    # Shoot arctium blaster
                    pygame.mixer.Sound.play(self.arct_blaster_sound)
                    self.arct_blaster.shoot(Vector2.copy(self.get(Transform).pos), self.get(Transform).angle)
                    inventory.InventoryManager.getInstance().arctium_count -= 1
                elif self.arct_blaster.cooldown <= 0:
                    pygame.mixer.Sound.play(self.empty_sound)

            # Craft hearts with ammo if selected and clicked
            # NOTE: hearts will not be crafted if the player has insufficient ammo (1 heart = 20 ammo)
            if inventory.InventoryManager.getInstance().is_used(4, events):
                if inventory.InventoryManager.getInstance().get_count(4) - 20 >= 0:
                    pygame.mixer.Sound.play(self.craft_sound)
                    inventory.InventoryManager.getInstance().ammo_count -= 20
                    inventory.InventoryManager.getInstance().heart_count += 1
                else:
                    pygame.mixer.Sound.play(self.empty_sound)
            
            # Apply heart effects if selected and clicked
            # NOTE: a heart will not be used if the player is already at maximum health, and if using a heart exceeds the maximum health, the player's health will be capped at the maximum
            if inventory.InventoryManager.getInstance().is_used(5, events):
                if self.maxHP > self.currentHP:
                    if self.currentHP + self.maxHP // 5 > self.maxHP:
                        self.currentHP = self.maxHP
                    else:
                        self.currentHP += self.maxHP // 5
                    pygame.mixer.Sound.play(self.heal_sound)
                    inventory.InventoryManager.getInstance().heart_count -= 1
                else:
                    pygame.mixer.Sound.play(self.empty_sound)

            # Craft ammo with Arctium crystals if selected and clicked
            # NOTE: ammo will not be crafted if the player has insufficient crystals (1 crystal = 10 ammo)
            if inventory.InventoryManager.getInstance().is_used(6, events):
                if inventory.InventoryManager.getInstance().get_count(6) - 1 >= 0:
                    pygame.mixer.Sound.play(self.craft_sound)
                    inventory.InventoryManager.getInstance().arctium_count -= 1
                    inventory.InventoryManager.getInstance().ammo_count += 10
                else:
                    pygame.mixer.Sound.play(self.empty_sound)
                    
    # Updating player-related entities in the dungeon levels
    def update(self, barriers, enemies, turrets, pistol, merc_pistol, arct_blaster, ammo, hearts, arctium, chest):
        # Update bullets
        self.pistol.update_bullets(barriers, enemies)
        self.merc_pistol.update_bullets(barriers, enemies)
        self.arct_blaster.update_bullets(barriers, enemies)

        # Update player speed from spider
        if self.invul > 0 and self.webbed:
            self.speed = self.base_speed // 2
            if self.speed == 0: self.speed += 1
        if self.invul <= 0 and self.webbed:
            self.webbed = False
            self.speed = self.base_speed

        # Get player hitbox for collisions
        hitbox = super().get_hitbox()
        
        # Enemy collisions
        for enemy in enemies:
            if pygame.Rect.colliderect(hitbox, enemy.get_hitbox()):
                # If no invul frames, take damage and gain invul frames
                if self.invul <= 0:
                    super().move(-self.direction)
                    self.moving = False
                    self.invul = 80
                    pygame.mixer.Sound.play(self.damage_sound)
                    self.currentHP -= enemy.damage
                    # If spider, slow player
                    if enemy.is_spider:
                        self.webbed = True
                    break

        # Turret bullet collisions
        for turret in turrets:
            if turret.damage_player:
                # If no invul frames, take damage and gain invul frames
                if self.invul <= 0:
                    super().move(-self.direction)
                    self.moving = False
                    self.invul = 80
                    pygame.mixer.Sound.play(self.turret_sound)
                    self.currentHP -= turret.damage
                    break
        
        # Item collection
        if pygame.Rect.colliderect(hitbox, pistol.get_rect()) and inventory.InventoryManager.getInstance().pistol_count == 0:
            pistol.collected = True
            inventory.InventoryManager.getInstance().pistol_count += 1
        if pygame.Rect.colliderect(hitbox, merc_pistol.get_rect()) and inventory.InventoryManager.getInstance().merc_pistol_count == 0:
            merc_pistol.collected = True
            inventory.InventoryManager.getInstance().merc_pistol_count += 1
        if pygame.Rect.colliderect(hitbox, arct_blaster.get_rect()) and inventory.InventoryManager.getInstance().arct_blaster_count == 0:
            arct_blaster.collected = True
            inventory.InventoryManager.getInstance().arct_blaster_count += 1
        for ammunition in ammo:
            if pygame.Rect.colliderect(hitbox, ammunition.get_rect()):
                ammunition.collected = True
                inventory.InventoryManager.getInstance().ammo_count += 10
        for heart in hearts:
            if pygame.Rect.colliderect(hitbox, heart.get_rect()):
                heart.collected = True
                inventory.InventoryManager.getInstance().heart_count += 1
        for crystal in arctium:
            if pygame.Rect.colliderect(hitbox, crystal.get_rect()):
                crystal.collected = True
                inventory.InventoryManager.getInstance().arctium_count += 1
        
        # Level clear condition: bringing arctium to a chest
        if pygame.Rect.colliderect(hitbox, chest.get_rect()) and inventory.InventoryManager.getInstance().arctium_count > 0:
             chest.collected = True
    
        self.update_player(barriers)
        
    # Update method for boss level
    def update_boss(self, barriers, boss:Boss):
        # Get player hitbox for collisions
        hitbox = super().get_hitbox()

        # Crystal collisions
        for crystal in boss.crystals:
            if pygame.Rect.colliderect(hitbox, crystal.get(Transform).get_hitbox()):
                if self.invul <= 0:
                    super().move(-self.direction)
                    self.moving = False
                    self.invul = 80
                    self.currentHP -= crystal.damage
                    pygame.mixer.Sound.play(self.damage_sound)
                    if crystal in boss.crystals:
                            boss.crystals.remove(crystal)
                
        self.update_player(barriers)

    # Common functions for both update methods
    def update_player(self, barriers):
        # Get player hitbox for collisions
        hitbox = super().get_hitbox()

        # If collided with a barrier, move the player back such that they don't clip through the barrier
        for barrier in barriers:
            if pygame.Rect.colliderect(hitbox, barrier):
                super().move(-self.direction)
                self.moving = False
                break

        # Update invincibility frames
        if self.invul > 0:
            self.invul -= 1            

        # If player is in invul, flicker sprite a few times per second
        if self.invul > 0:
            if self.invul % 10 == 0:
                self.flicker = not self.flicker
            if self.flicker == True:
                super().get(Sprite).set_sprite(self.spriteSet[2])
                return
            
        # Update Sprite based on movement
        if self.direction == Vector2(0,0):
            self.moving = False
        if self.moving == True:
            super().get(Sprite).set_sprite(self.spriteSet[1])
        else:
            super().get(Sprite).set_sprite(self.spriteSet[0])

        # If weapon is being fired, update sprite regardless of movement
        if self.pistol.shooting == True or self.merc_pistol.shooting or self.arct_blaster.shooting:
            super().get(Sprite).set_sprite(self.spriteSet[0])

    # Moving player
    def move(self):
        super().move(self.direction)

    # Drawing player to screen
    def render(self, screen):
        # Face the mouse (for aiming)
        self.rotate_towards(pygame.mouse.get_pos())

        # Render bullets for all weapons
        self.pistol.render_bullets(screen)
        self.merc_pistol.render_bullets(screen)
        self.arct_blaster.render_bullets(screen)

        # Draw to screen
        super().render(screen)

    # Method to save player information to a json file
    def save_player_data(self):
        try:
            with open('player_data.json') as json_file:
                player_data_dict = json.load(json_file)      
        except:
            print("Error writing to JSON file")
        
        # Storing inventory collection
        ammo = inventory.InventoryManager.getInstance().ammo_count 
        hearts = inventory.InventoryManager.getInstance().heart_count
        arctium = inventory.InventoryManager.getInstance().arctium_count  
        
        # Dungeon counter
        dungeons = ui_elements.HUD.getInstance().dungeons

        # Player stats
        attributes = {"maxHP":math.floor(self.maxHP),
                     "kills":self.kills,
                     "spriteSet": self.spriteSet,
                     "base_speed":self.base_speed,
                     "pistol":{
                        "weaponDmg":self.pistol.damage,
                        "weaponFireRate":self.pistol.fire_rate,
                        "weaponImgPath":self.pistol.img_path
                        },
                     "merc_pistol":{
                        "weaponDmg":self.merc_pistol.damage,
                        "weaponFireRate":self.merc_pistol.fire_rate,
                        "weaponImgPath":self.merc_pistol.img_path
                        },
                     "arct_blaster":{
                        "weaponDmg":self.arct_blaster.damage,
                        "weaponFireRate":self.arct_blaster.fire_rate,
                        "weaponImgPath":self.arct_blaster.img_path
                        },
                     "ammo":ammo,
                     "hearts": hearts,
                     "arctium": arctium,     
                     "dungeons": dungeons
                    }

        # Saving information to json
        with open("player_data.json", 'w') as f:
            json.dump(attributes, f)

    # Method to set player attributes and inventory counts from json file
    def set_player(self):
        try:
            with open('player_data.json') as json_file:
                player_data_dict = json.load(json_file)
        except:
            print("Error in reading player_data file")
            return

        # Assign attributes to player
        for attribute in list(player_data_dict.items())[:-1]:
            if attribute != "pistol" and attribute != "merc_pistol" and attribute != "arct_blaster":
                setattr(self, attribute[0], attribute[1])

        # Set base variables
        self.speed = self.base_speed
        self.currentHP = self.maxHP

        # Set weapons using json data
        self.pistol = Weapon(0,0,player_data_dict["pistol"]["weaponImgPath"],player_data_dict["pistol"]["weaponDmg"], player_data_dict["pistol"]["weaponFireRate"])
        self.merc_pistol = Weapon(0,0,player_data_dict["merc_pistol"]["weaponImgPath"],player_data_dict["merc_pistol"]["weaponDmg"], player_data_dict["merc_pistol"]["weaponFireRate"])
        self.arct_blaster = Weapon(0,0,player_data_dict["arct_blaster"]["weaponImgPath"],player_data_dict["arct_blaster"]["weaponDmg"], player_data_dict["arct_blaster"]["weaponFireRate"])

        # Update inventory manager based on player's inventory
        # NOTE: Guns are considered to be collected if their recorded damage is > 0
        if self.pistol.damage > 0:
            inventory.InventoryManager.getInstance().pistol_count += 1
        if self.merc_pistol.damage > 0:
            inventory.InventoryManager.getInstance().merc_pistol_count += 1
        if self.arct_blaster.damage > 0:
            inventory.InventoryManager.getInstance().arct_blaster_count += 1
        
        # Save ammo if greater than starting ammo
        if player_data_dict["ammo"] > 10:
            inventory.InventoryManager.getInstance().ammo_count = player_data_dict["ammo"]

        # Save heart and arctium counts
        inventory.InventoryManager.getInstance().heart_count = player_data_dict["hearts"]
        inventory.InventoryManager.getInstance().arctium_count = player_data_dict["arctium"]

        # Save dungeon counts
        ui_elements.HUD.getInstance().dungeons = player_data_dict["dungeons"]