# Screen Class for the game over screen
import pygame
import json

from screens.screen_base import ScreenBase

import src.ui.ui_elements as ui_elements
import src.inventory.inventory_manager as inventory

class GameOver(ScreenBase):
    def __init__(self, current_world: str):
        ScreenBase.__init__(self)

        # Store current world
        self.current_world = current_world

        # Background image
        self.you_died = pygame.transform.smoothscale(
            pygame.image.load("assets/you_died.jpeg"), (1216, 832)
        )

        # Buttons
        self.retry_button = ui_elements.Button("RETRY", 490, 575)
        self.give_up_button = ui_elements.Button("GIVE UP", 700, 575)
        self.go_back_button = ui_elements.Button("GO BACK", 595, 675)

        # Play sound effect
        self.level_end = pygame.mixer.Sound("assets/sounds/music/level_end.wav")
        self.level_end.set_volume(0.15)
        pygame.mixer.Sound.play(self.level_end)

    # Process button clicks
    def process_input(self, events: list):
        for event in events:
            # Return to the world to retry
            if self.retry_button.is_clicked(event):
                if (self.current_world == "boss"):
                    from screens.boss_screen import BossScreen
                    self.switch_to_scene(BossScreen())
                else:
                    from screens.world_screen import WorldScreen
                    self.switch_to_scene(WorldScreen(self.current_world))
            # Return to main menu
            if self.give_up_button.is_clicked(event):
                from screens.start_screens import StartScreen
                self.switch_to_scene(StartScreen())
            
            # For the boss level, return to the cave to continue grinding
            if self.go_back_button.is_clicked(event) and self.current_world == "boss":
                from screens.world_screen import WorldScreen
                self.switch_to_scene(WorldScreen("caveMap"))
            

    def update(self):
        ui_elements.Cursor.getInstance().update()  # Update custom cursor position

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))

        # Background image rendering
        screen.blit(self.you_died, self.you_died.get_rect())

        # Button rendering
        self.retry_button.render_button(screen)
        self.give_up_button.render_button(screen)

        if (self.current_world == "boss"):
            self.go_back_button.render_button(screen)

        # Cursor rendering
        ui_elements.Cursor.getInstance().render(screen)

# Screen Class for the win screen
class LevelClear(ScreenBase):
    def __init__(self, current_world: str):
        ScreenBase.__init__(self)
        
        # Store current world
        self.current_world = current_world

        # Load the world data
        player_data = json.load(open("player_data.json"))

        # Dungeon cleared image
        self.dungeon_win = pygame.transform.smoothscale(pygame.image.load("assets/dungeon_win.jpeg"), (1216, 832))

        # Player statistics
        self.max_hp = player_data["maxHP"]
        self.enemies_slain = player_data["kills"]
        self.arctium_count = inventory.InventoryManager.getInstance().arctium_count

        # Text for player statistics
        self.hp_text = ui_elements.display_font.render(f"MAX HP: {self.max_hp}", True, (255, 255, 255))
        self.slain_text = ui_elements.display_font.render(f"ENEMIES SLAIN: {self.enemies_slain}", True, (255, 255, 255))
        self.arctium_text = ui_elements.display_font.render(f"ARCTIUM COUNT: {self.arctium_count}", True, (255, 255, 255))

        # Buttons
        self.continue_button = ui_elements.Button("CONTINUE GRINDING", 478, 775)
        self.boss_button = ui_elements.Button("DELVE DEEPER", 735, 775)

        # Play sound effect
        self.level_end = pygame.mixer.Sound("assets/sounds/music/level_end.wav")
        self.level_end.set_volume(0.15)
        pygame.mixer.Sound.play(self.level_end)

    # Process button clicks
    def process_input(self, events: list):
        for event in events:
            # Swap dungeons
            if self.continue_button.is_clicked(event):
                from screens.world_screen import WorldScreen
                if self.current_world == "caveMap":
                    self.switch_to_scene(WorldScreen("ruinMap"))
                else:
                    self.switch_to_scene(WorldScreen("caveMap"))
            # Move to boss screen
            if self.boss_button.is_clicked(event):
                from screens.boss_screen import BossScreen
                
                self.switch_to_scene(BossScreen())

    def update(self):
        ui_elements.Cursor.getInstance().update()  # Update custom cursor position

    def render(self, screen: pygame.Surface):

        # Background rendering
        screen.blit(self.dungeon_win, self.dungeon_win.get_rect())

        # Text Rendering
        screen.blit(self.hp_text, self.hp_text.get_rect(x = 375, y = 525))
        screen.blit(self.slain_text, self.slain_text.get_rect(x = 375, y = 575))
        screen.blit(self.arctium_text, self.arctium_text.get_rect(x = 375, y = 625))

        # Button rendering
        self.continue_button.render_button(screen)
        self.boss_button.render_button(screen)

        # Cursor rendering
        ui_elements.Cursor.getInstance().render(screen)

# Screen Class for the victory screen
class WinScreen(ScreenBase):
    def __init__(self):
        ScreenBase.__init__(self)
    
        # Load the world data
        player_data = json.load(open("player_data.json"))

        # Dungeon cleared image
        self.beast_win = pygame.transform.smoothscale(pygame.image.load("assets/beast_win.jpeg"), (1216, 832))

        # Player statistics
        self.max_hp = player_data["maxHP"]
        self.enemies_slain = player_data["kills"]
        self.arctium_count = inventory.InventoryManager.getInstance().arctium_count

        # Text for player statistics
        self.hp_text = ui_elements.display_font.render(f"MAX HP: {self.max_hp}", True, (255, 255, 255))
        self.slain_text = ui_elements.display_font.render(f"ENEMIES SLAIN: {self.enemies_slain}", True, (255, 255, 255))
        self.arctium_text = ui_elements.display_font.render(f"ARCTIUM COUNT: {self.arctium_count}", True, (255, 255, 255))

        # Buttons
        self.continue_button = ui_elements.Button("CONTINUE", 505, 775)
        self.return_button = ui_elements.Button("RETURN TO MAIN MENU", 685, 775)

    # Process buttons
    def process_input(self, events: list):
        for event in events:
            # Return to the beginning dungeon
            if self.continue_button.is_clicked(event):
                from screens.world_screen import WorldScreen

                self.switch_to_scene(WorldScreen("ruinMap"))    
            # Return to main menu
            if self.return_button.is_clicked(event):
                from screens.start_screens import StartScreen

                self.switch_to_scene(StartScreen())

    def update(self):
        ui_elements.Cursor.getInstance().update() # Update custom cursor position

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))

        # Background rendering
        screen.blit(self.beast_win, self.beast_win.get_rect())

        # Text Rendering
        screen.blit(self.hp_text, self.hp_text.get_rect(x = 375, y = 525))
        screen.blit(self.slain_text, self.slain_text.get_rect(x = 375, y = 575))
        screen.blit(self.arctium_text, self.arctium_text.get_rect(x = 375, y = 625))

        # Button rendering
        self.continue_button.render_button(screen)
        self.return_button.render_button(screen)

        # Cursor rendering
        ui_elements.Cursor.getInstance().render(screen)