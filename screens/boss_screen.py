import pygame
from pygame.math import Vector2
from pygame import mixer

from screens.screen_base import ScreenBase

import src.lib.tilemap as tilemap
import src.ui.ui_elements as ui_elements
import src.inventory.inventory_manager as inventory

from src.entity.player import Player
from src.entity.arctbeast import Boss

class BossScreen(ScreenBase):
    def __init__(self):
        ScreenBase.__init__(self)

        # Visual variables
        self.background = pygame.transform.smoothscale(
            pygame.image.load("assets/maps/arctbeastCave.jpg"), (1216, 832)
        )
        self.background_rect = self.background.get_rect()

        # Music
        mixer.music.load("assets/sounds/music/arctbeast.wav")
        mixer.music.set_volume(0.15)
        mixer.music.play()

        # Extracting barriers from the TileMap
        self.tilemap = tilemap.TiledMap("assets/maps/arctbeast.tmx")
        self.barriers = self.tilemap.get_rects_in_layer("Barriers")

        # Initialize boss
        self.boss = Boss()

        # Initialize player
        self.player = Player(position=Vector2(640, 736))
        self.player.set_player()

    def process_input(self, events: list):
        self.player.process_input(events)

        # Update inventory selection based on keyboard input (1-6)
        inventory.InventoryManager.getInstance().set_selected(events)

    def update(self):
        # Restart music if it's done playing
        if mixer.music.get_busy() == False:
            mixer.music.play()

        ui_elements.Cursor.getInstance().update() # Update custom cursor position

        # Update player
        self.player.move()
        self.player.update_boss(self.barriers,self.boss)

        # Update bullets
        self.player.pistol.update_boss(self.boss)
        self.player.merc_pistol.update_boss(self.boss)
        self.player.arct_blaster.update_boss(self.boss)

        # Update arctbeast
        self.boss.update()

        ui_elements.HUD.getInstance().update(self.player) # Update HUD information

        # If Player died, die
        if self.player.currentHP <= 0:
            mixer.music.stop()
            from screens.end_screens import GameOver
            self.switch_to_scene(GameOver("boss"))

        # If boss died, win
        if self.boss.hp <= 0:
            from screens.end_screens import WinScreen
            # Save ammo count
            self.player.save_player_data()
            self.switch_to_scene(WinScreen())
        

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))

        # Render background 
        screen.blit(self.background, self.background_rect)

        # Render player
        self.player.render(screen)

        # Render arctbeast
        self.boss.render(screen)

        # Render the HUD
        ui_elements.HUD.getInstance().render(screen)

        # Cursor rendering
        ui_elements.Cursor.getInstance().render(screen)

    def switch_to_scene(self, next_scene):
        self.next = next_scene