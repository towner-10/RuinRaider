import pygame
import json
from pygame import mixer

from screens.screen_base import ScreenBase
from screens.world_screen import WorldScreen

import src.ui.ui_elements as ui_elements
import src.inventory.inventory_manager as inventory

from src.entity.player import Player

# Screen Class for the loading screen
class SplashScreen(ScreenBase):
    def __init__(self, fade_in_time=2, fade_out_time=2.3):
        ScreenBase.__init__(self)

        # Music
        mixer.music.load("assets/sounds/music/splash_sound.wav")
        mixer.music.set_volume(0.1)
        mixer.music.play()

        # Variables for fade effect
        self.start_time = pygame.time.get_ticks()
        self.fade_in_time = fade_in_time
        self.fade_out_time = fade_out_time
        self.alpha = 0

        # Team name text
        self.text = ui_elements.display_font.render("TEAM 96", True, (255, 255, 255))

    def process_input(self, events):
        pass

    def update(self):
        # Restart music if it's done playing
        if mixer.music.get_busy() == False:
            mixer.music.play()

        # Get the time in seconds
        seconds = (pygame.time.get_ticks() - self.start_time) / 1000

        # Fade in and out animation
        if seconds < self.fade_in_time:
            # Fading in animation scaling with the fade in time
            self.alpha = (255 / self.fade_in_time) * seconds
        elif seconds > self.fade_in_time and seconds < (
            self.fade_in_time + self.fade_out_time
        ):
            # Fading out animation
            self.alpha = 255 - (255 / self.fade_out_time) * (
                seconds - self.fade_in_time
            )
        else:
            mixer.music.stop()
            self.switch_to_scene(StartScreen())

    def render(self, screen):
        # Black screen
        screen.fill((0, 0, 0))

        # Put text
        self.text.set_alpha(self.alpha)
        text_rect = self.text.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2)
        )
        screen.blit(self.text, text_rect)


# Screen Class for the main menu
class StartScreen(ScreenBase):
    def __init__(self, fade_in_time=2):
        ScreenBase.__init__(self)

        # Alpha variable for fading animation
        self.start_time = pygame.time.get_ticks()
        self.alpha = 0
        self.fade_in_time = fade_in_time

        # Background
        self.menu_art = pygame.transform.smoothscale(
            pygame.image.load("assets/main_menu.jpeg"), (1216, 832)
        )

        # Music
        mixer.music.load("assets/sounds/music/main_sound.wav")
        mixer.music.set_volume(0.1)
        mixer.music.play()

        # Buttons
        self.start_button = ui_elements.Button("START GAME", 415, 575)
        self.customize_button = ui_elements.Button("CUSTOMIZE CHARACTER", 630, 575)
        self.info_button = ui_elements.Button("INFO", 810, 575)

    # Process buttons
    def process_input(self, events):
        for event in events:
            # Move to first level
            if self.start_button.is_clicked(event):
                mixer.music.stop()
                self.switch_to_scene(WorldScreen("ruinMap"))
            
            # Move to customization screen
            if self.customize_button.is_clicked(event):
                mixer.music.stop()
                self.switch_to_scene(CustomizationScreen())
            
            # Move to information screen
            if self.info_button.is_clicked(event):
                mixer.music.stop()
                self.switch_to_scene(InfoScreen())

    def update(self):
        # Restart music if it's done playing
        if mixer.music.get_busy() == False:
             mixer.music.play()

        # Fade-in effect
        seconds = (pygame.time.get_ticks() - self.start_time) / 1000
        if seconds < self.fade_in_time:
            self.alpha = (255 / self.fade_in_time) * seconds

        ui_elements.Cursor.getInstance().update() # Update custom cursor position    

    def render(self, screen):
        screen.fill((0, 0, 0))

        # Create the menu image
        self.menu_art.set_alpha(self.alpha)
        menu_rect = self.menu_art.get_rect()
        screen.blit(self.menu_art, menu_rect)

        # Button rendering
        self.start_button.render_button(screen)
        self.customize_button.render_button(screen)
        self.info_button.render_button(screen)

        ui_elements.Cursor.getInstance().render(screen) # Render custom cursor


# Screen Class for the customization screen
class CustomizationScreen(ScreenBase):
    def __init__(self):
        ScreenBase.__init__(self)

        # Dummy player object to save to JSON
        self.player = Player()
        self.player.set_player()

        # Visual/Audio variables
        self.menu_art = pygame.transform.smoothscale(
            pygame.image.load("assets/maps/arctbeastCave.jpg"), (1216, 832)
        )

        # Icons for the 3 characters
        self.blue = pygame.transform.smoothscale(
            pygame.image.load("assets\sprites\mercenary.jpg"), (256, 256)
        )
        self.blue_rect = self.blue.get_rect().move(200, 256)
        self.blue.set_alpha(128)

        self.brown = pygame.transform.smoothscale(
            pygame.image.load("assets\sprites\heavy.jpg"), (256, 256)
        )
        self.brown_rect = self.brown.get_rect().move(480, 256)
        self.brown.set_alpha(128)

        self.green = pygame.transform.smoothscale(
            pygame.image.load("assets\sprites\skirmisher.jpg"), (256, 256)
        )
        self.green_rect = self.green.get_rect().move(760, 256)
        self.green.set_alpha(128)

        # Music
        mixer.music.load("assets/sounds/music/splash_sound.wav")
        mixer.music.set_volume(0.1)
        mixer.music.play()

        # Text
        self.heading_text = ui_elements.display_font.render(
            "SELECT YOUR CHARACTER", True, (255, 255, 255)
        )
        self.heading_text_rect = self.heading_text.get_rect(x=300, y=150)

        self.blue_text = ui_elements.main_font.render("DEFAULT", True, (255, 255, 255))
        self.blue_text_rect = self.blue_text.get_rect(x=290, y=600)

        self.brown_text = ui_elements.main_font.render(
            "↑ STRENGTH   ↓ SPEED", True, (255, 255, 255)
        )
        self.brown_text_rect = self.brown_text.get_rect(x=515, y=600)

        self.green_text = ui_elements.main_font.render(
            "↓ STRENGTH   ↑ SPEED", True, (255, 255, 255)
        )
        self.green_text_rect = self.green_text.get_rect(x=790, y=600)

        # Buttons
        self.blue_select = ui_elements.Button("MERCENARY", 325, 550)
        self.brown_select = ui_elements.Button("HEAVY", 610, 550)
        self.green_select = ui_elements.Button("SKIRMISHER", 885, 550)
        self.save = ui_elements.Button("SAVE", 565, 700)
        self.cancel = ui_elements.Button("BACK", 650, 700)

        # Variable to track selected button
        self.selected = 0

    def process_input(self, events):
        for event in events:
            # Selecting the character
            if self.blue_select.is_clicked(event):
                self.selected = 1

                # Highlight blue
                self.blue.set_alpha(255)
                self.brown.set_alpha(128)
                self.green.set_alpha(128)

            if self.brown_select.is_clicked(event):
                self.selected = 2

                # Highlight brown
                self.blue.set_alpha(128)
                self.brown.set_alpha(255)
                self.green.set_alpha(128)

            if self.green_select.is_clicked(event):
                self.selected = 3

                # Highlight green
                self.blue.set_alpha(128)
                self.brown.set_alpha(128)
                self.green.set_alpha(255)

            # Saving
            if self.save.is_clicked(event):
                # Update player stats and save information to JSON
                if self.selected == 1:
                    # Changing HP based on previous class
                    if self.player.base_speed == 1:
                        self.player.maxHP /= 2
                    if self.player.base_speed == 4:
                        self.player.maxHP *= 2

                    # Setting speed and sprite
                    self.player.base_speed = 2
                    self.player.spriteSet = ["assets/sprites/manBlue/manBlue_gunStand.png", "assets/sprites/manBlue/manBlue_gunWalk.png", "assets/sprites/empty_image.png"]
                if self.selected == 2:
                    # Changing HP based on previous class
                    if self.player.base_speed == 2:
                        self.player.maxHP *= 2
                    if self.player.base_speed == 4:
                        self.player.maxHP *= 3

                    # Setting speed and sprite
                    self.player.base_speed = 1
                    self.player.spriteSet = ["assets/sprites/manBrown/manBrown_gunStand.png", "assets/sprites/manBrown/manBrown_gunWalk.png", "assets/sprites/empty_image.png"]
                if self.selected == 3:
                    # Changing HP based on previous class
                    if self.player.base_speed == 2:
                        self.player.maxHP /= 2
                    if self.player.base_speed == 1:
                        self.player.maxHP /= 3

                    # Setting speed and sprite
                    self.player.base_speed = 4
                    self.player.spriteSet = ["assets/sprites/woman/womanGreen_gunStand.png", "assets/sprites/woman/womanGreen_gunWalk.png", "assets/sprites/empty_image.png"]
                
                # Save new information in player json
                self.player.save_player_data()

                # Return to main menu
                self.switch_to_scene(StartScreen())

            # Return to main screen without changing anything
            if self.cancel.is_clicked(event):
                mixer.music.stop()
                self.switch_to_scene(StartScreen())

    def update(self):
        # Restart music if it's done playing
        if mixer.music.get_busy() == False:
            mixer.music.play()

        ui_elements.Cursor.getInstance().update() # Update custom cursor position

    def render(self, screen):
        screen.fill((0, 0, 0))

        # Create the menu image
        menu_rect = self.menu_art.get_rect()
        screen.blit(self.menu_art, menu_rect)

        # Character rendering
        screen.blit(self.blue, self.blue_rect)
        screen.blit(self.brown, self.brown_rect)
        screen.blit(self.green, self.green_rect)

        # Text rendering
        screen.blit(self.heading_text, self.heading_text_rect)
        screen.blit(self.blue_text, self.blue_text_rect)
        screen.blit(self.green_text, self.green_text_rect)
        screen.blit(self.brown_text, self.brown_text_rect)

        # Button rendering
        self.blue_select.render_button(screen)
        self.brown_select.render_button(screen)
        self.green_select.render_button(screen)
        self.save.render_button(screen)
        self.cancel.render_button(screen)

        # Cursor rendering
        ui_elements.Cursor.getInstance().render(screen)

# Screen Class for the information screen
class InfoScreen(ScreenBase):
    def __init__(self):
        ScreenBase.__init__(self)
        self.infographic = pygame.transform.smoothscale(pygame.image.load("assets/infographic.jpeg"), (1216, 832))

        # Load music
        mixer.music.load("assets/sounds/music/splash_sound.wav")
        mixer.music.set_volume(0.1)
        mixer.music.play()

        # Buttons
        self.reset = ui_elements.Button("RESET PROGRESS", 850, 700)
        self.cancel = ui_elements.Button("BACK", 1000, 700)
        
    # Process buttons
    def process_input(self, events):
        for event in events:
            # Reset save data
            if self.reset.is_clicked(event):
                self.reset_save_data()

            # Return to main menu
            if self.cancel.is_clicked(event):
                mixer.music.stop()
                self.switch_to_scene(StartScreen()) # Return to the main screen
    
    # Method to reset all save data
    def reset_save_data(self):
        # Reset inventory
        inventory.InventoryManager.getInstance().pistol_count = 0
        inventory.InventoryManager.getInstance().merc_pistol_count = 0
        inventory.InventoryManager.getInstance().arct_blaster_count = 0
        inventory.InventoryManager.getInstance().ammo_count = 10
        inventory.InventoryManager.getInstance().heart_count = 0
        inventory.InventoryManager.getInstance().arctium_count = 0
        inventory.InventoryManager.getInstance().chest_count = 0

        try:
            with open('player_data.json') as json_file:
                player_data_dict = json.load(json_file)      
        except:
            print("error writing to JSON file")

        # Reset player attributes       
        attributes = {"maxHP":100,
                     "kills":0,
                     "spriteSet":[
                            "assets/sprites/manBlue/manBlue_gunStand.png",
                            "assets/sprites/manBlue/manBlue_gunWalk.png",
                            "assets/sprites/empty_image.png",
                            ],
                     "base_speed":2,
                    "pistol":{
                        "weaponDmg":0,
                        "weaponFireRate":0,
                        "weaponImgPath":"assets/sprites/items/pistol.png"
                        },
                     "merc_pistol":{
                        "weaponDmg":0,
                        "weaponFireRate":0,
                        "weaponImgPath":"assets/sprites/items/merc_pistol.png"
                        },
                     "arct_blaster":{
                        "weaponDmg":0,
                        "weaponFireRate":0,
                        "weaponImgPath":"assets/sprites/items/arct_blaster.png"
                        },
                     "ammo":10,
                     "hearts": 0,
                     "arctium":0,
                     "dungeons": 0
                    }
        
        # Save resetted player to json
        with open("player_data.json", 'w') as f:
            json.dump(attributes, f)

    def update(self):
        # Restart music if it's done playing
        if mixer.music.get_busy() == False:
            mixer.music.play()
        ui_elements.Cursor.getInstance().update() # Update custom cursor position

    def render(self, screen):
        screen.fill((0, 0, 0))

        # Background rendering
        screen.blit(self.infographic, self.infographic.get_rect())

        # Button rendering
        self.cancel.render_button(screen)
        self.reset.render_button(screen)

        # Cursor rendering
        ui_elements.Cursor.getInstance().render(screen)