import pygame

from src.entity.player import Player
import src.inventory.inventory_manager as inventory

# Initialize the PyGame font library
pygame.font.init()

# Display font (for headers and large standalone text)
display_font = pygame.font.Font("assets/monumentextended-regular.otf", 36)

# Main font (for smaller text in dialogs and buttons)
main_font = pygame.font.Font("assets/GolosText-Regular.ttf", 16)

# Button class (a button object takes as parameters the button text, the button's x-position on the screen, and the button's y-position on the screen)
class Button:
    def __init__(self, text, x: float, y: float):
        self.text = text
        self.x = x
        self.y = y

        self.click_sound = pygame.mixer.Sound("assets/sounds/effects/tick_001.ogg")
        self.click_sound.set_volume(0.3)

        self.rect = pygame.Rect(x, y, 11 * len(text) + 20, 40)
        self.rect.center = (x, y)

    # Render the button onto the screen
    def render_button(self, screen: pygame.Surface):
        # Set button and text color depending on hover state (hovered versus unhovered)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            button_color = (5, 13, 42)
            text_color = (255, 255, 255)
        else:
            button_color = (255, 255, 255)
            text_color = (5, 13, 42)

        # Draw the button and its text
        pygame.draw.rect(screen, button_color, self.rect)

        text_obj = main_font.render(self.text, True, text_color)
        text_rect = text_obj.get_rect(center=self.rect.center)
        screen.blit(text_obj, text_rect)

    # Detect when a button is clicked
    def is_clicked(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.play(self.click_sound)
                return True
        return False

# Cursor class to display the custom cursor
class Cursor:
    __instance = None

    @staticmethod
    def getInstance():
        """Static access method."""
        if Cursor.__instance == None:
            Cursor.__instance = Cursor()
        return Cursor.__instance
    
    def __init__(self):
        """Virtually private constructor."""
        if Cursor.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Cursor.__instance = self
            self.image = pygame.transform.smoothscale(pygame.image.load("assets/sprites/cursor.png"), (28, 33))
            self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.center = pygame.mouse.get_pos()

        # Position correction to account for cursor shape
        self.rect.x += 10
        self.rect.y += 15

    def render(self, screen):
        screen.blit(self.image, self.rect)

# HUD class to display screen elements (i.e., health, inventory, and FPS)
class HUD:
    __instance = None

    @staticmethod
    def getInstance():
        """Static access method."""
        if HUD.__instance == None:
            HUD.__instance = HUD()
        return HUD.__instance
    
    def __init__(self):
        """Virtually private constructor."""
        if HUD.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            HUD.__instance = self
            self.selected = 0
            self.health = 0
            self.max_health = 0
            self.kills = 0
            self.dungeons = 0
            self.fps = 0

            # Create empty inventory slot images and rects
            self.pistol_inv_empty = pygame.image.load("assets/sprites/inventory/pistol_inv_empty.jpg")
            self.merc_pistol_inv_empty = pygame.image.load("assets/sprites/inventory/merc_pistol_inv_empty.jpg")
            self.arct_blaster_inv_empty = pygame.image.load("assets/sprites/inventory/arct_blaster_inv_empty.jpg")
            self.ammo_inv_empty = pygame.image.load("assets/sprites/inventory/ammo_inv_empty.jpg")
            self.heart_inv_empty = pygame.image.load("assets/sprites/inventory/heart_inv_empty.jpg")
            self.arctium_inv_empty = pygame.image.load("assets/sprites/inventory/arctium_inv_empty.jpg")

            self.pistol_inv_empty_rect = self.pistol_inv_empty.get_rect(x = 411, y = 768)
            self.merc_pistol_inv_empty_rect = self.merc_pistol_inv_empty.get_rect(x = 477, y = 768)
            self.arct_blaster_inv_empty_rect = self.arct_blaster_inv_empty.get_rect(x = 543, y = 768)
            self.ammo_inv_empty_rect = self.ammo_inv_empty.get_rect(x = 609, y = 768)
            self.heart_inv_empty_rect = self.heart_inv_empty.get_rect(x = 675, y = 768)
            self.arctium_inv_empty_rect = self.arctium_inv_empty.get_rect(x = 741, y = 768)

            # Create full inventory slot images and rects
            self.pistol_inv = pygame.image.load("assets/sprites/inventory/pistol_inv.jpg")
            self.merc_pistol_inv = pygame.image.load("assets/sprites/inventory/merc_pistol_inv.jpg")
            self.arct_blaster_inv = pygame.image.load("assets/sprites/inventory/arct_blaster_inv.jpg")
            self.ammo_inv = pygame.image.load("assets/sprites/inventory/ammo_inv.jpg")
            self.heart_inv = pygame.image.load("assets/sprites/inventory/heart_inv.jpg")
            self.arctium_inv = pygame.image.load("assets/sprites/inventory/arctium_inv.jpg")

            self.pistol_inv_rect = self.pistol_inv.get_rect(x = 411, y = 768)
            self.merc_pistol_inv_rect = self.merc_pistol_inv.get_rect(x = 477, y = 768)
            self.arct_blaster_inv_rect = self.arct_blaster_inv.get_rect(x = 543, y = 768)
            self.ammo_inv_rect = self.ammo_inv.get_rect(x = 609, y = 768)
            self.heart_inv_rect = self.heart_inv.get_rect(x = 675, y = 768)
            self.arctium_inv_rect = self.arctium_inv.get_rect(x = 741, y = 768)

            # Create image and rect for inventory slot selection indicator
            self.inv_select = pygame.image.load("assets/sprites/inventory/inv_select.png")
            self.inv_select_rect = self.inv_select.get_rect(y = 768)

    # Update method to update player's conditions
    def update(self, player: Player):
        self.health = player.currentHP
        self.max_health = player.maxHP
        self.kills = player.kills
        self.selected = inventory.InventoryManager.getInstance().selected

    # Render the HUD onto a screen
    def render(self, screen: pygame.Surface):
        
        # Create and draw health bar elements
        if (self.health / self.max_health) < 0.25: # Critically low health
            health_color = (237, 28, 36)
        elif (self.health / self.max_health) > 0.25 and (self.health / self.max_health) < 0.75: # Moderate health
            health_color = (255, 201, 14)
        else:
            health_color = (34, 177, 76) # High health
        
        health_bar = pygame.Rect(64, 38, 200, 20)
        health_bar_fill = (64, 38, self.health / self.max_health * 200, 20)
        
        health_text = main_font.render(str(int(self.health)) + "/" + str(int(self.max_health)), True, health_color)
        health_text_rect = health_text.get_rect(x = 280, y = 37)

        strength_level = main_font.render("STRENGTH LEVEL: " + str(int(self.max_health // 100)), True, (255, 255, 255))
        strength_level_rect = strength_level.get_rect(x = 375, y = 37)

        kill_count = main_font.render("ENEMIES SLAIN: " + str(self.kills), True, (255, 255, 255))
        kill_count_rect = kill_count.get_rect(x = 570, y = 37)

        dungeon_count = main_font.render("DUNGEONS CLEARED: " + str(self.dungeons), True, (255, 255, 255))
        dungeon_count_rect = dungeon_count.get_rect(x = 750, y = 37)

        pygame.draw.rect(screen, (255, 255, 255), health_bar)
        pygame.draw.rect(screen, health_color, health_bar_fill)
        screen.blit(health_text, health_text_rect)
        screen.blit(strength_level, strength_level_rect)
        screen.blit(kill_count, kill_count_rect)
        screen.blit(dungeon_count, dungeon_count_rect)

        # Draw empty inventory slots
        screen.blit(self.pistol_inv_empty, self.pistol_inv_empty_rect)
        screen.blit(self.merc_pistol_inv_empty, self.merc_pistol_inv_empty_rect)
        screen.blit(self.arct_blaster_inv_empty, self.arct_blaster_inv_empty_rect)
        screen.blit(self.ammo_inv_empty, self.ammo_inv_empty_rect)
        screen.blit(self.heart_inv_empty, self.heart_inv_empty_rect)
        screen.blit(self.arctium_inv_empty, self.arctium_inv_empty_rect)

        # Draw full inventory slots (and item count where applicable) depending on the item counts of the player
        if inventory.InventoryManager.getInstance().pistol_count > 0:
            self.render_slot(screen, self.pistol_inv, self.pistol_inv_rect)
        
        if inventory.InventoryManager.getInstance().merc_pistol_count > 0:
            self.render_slot(screen, self.merc_pistol_inv, self.merc_pistol_inv_rect)
        
        if inventory.InventoryManager.getInstance().arct_blaster_count > 0:
            self.render_slot(screen, self.arct_blaster_inv, self.arct_blaster_inv_rect)
        
        if inventory.InventoryManager.getInstance().ammo_count > 0:
            self.render_slot(screen, self.ammo_inv, self.ammo_inv_rect, True, inventory.InventoryManager.getInstance().ammo_count, 614)
        
        if inventory.InventoryManager.getInstance().heart_count > 0:
            self.render_slot(screen, self.heart_inv, self.heart_inv_rect, True, inventory.InventoryManager.getInstance().heart_count, 680)
        
        if inventory.InventoryManager.getInstance().arctium_count > 0:
            self.render_slot(screen, self.arctium_inv, self.arctium_inv_rect, True, inventory.InventoryManager.getInstance().arctium_count, 746)

        # Highlight an inventory slot based on item selection
        if self.selected == 2:
            self.inv_select_rect.x = 477
        elif self.selected == 3:
            self.inv_select_rect.x = 543
        elif self.selected == 4:
            self.inv_select_rect.x = 609
        elif self.selected == 5:
            self.inv_select_rect.x = 675
        elif self.selected == 6:
            self.inv_select_rect.x = 741
        else:
            self.inv_select_rect.x = 411 # Select first slot by default
        
        screen.blit(self.inv_select, self.inv_select_rect)

        # Create and draw FPS text
        fps_text = main_font.render(str(int(self.fps)) + " FPS", True, (75, 75, 75))
        fps_text_rect = fps_text.get_rect(x = 1123, y = 13)
        screen.blit(fps_text, fps_text_rect)

    # Helper function for main HUD render method
    def render_slot(self, screen: pygame.Surface, image, rect, stackable = False, count = None, x_pos = None):
        screen.blit(image, rect)

        # Draw item count where applicable
        if stackable:
            item_count = main_font.render(str(count), True, (255, 255, 255))
            item_rect = item_count.get_rect(x = x_pos, y = 803)
            screen.blit(item_count, item_rect)