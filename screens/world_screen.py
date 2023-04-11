import pygame
import json
import random

import threading
from pygame.math import Vector2
from pygame import mixer

import src.lighting.lighting as lighting
import src.lib.tilemap as tilemap
import src.math.a_star as a_star
from src.lib.navmesh import Navmesh

from screens.screen_base import ScreenBase
from screens.end_screens import GameOver, LevelClear

import src.ui.ui_elements as ui_elements
import src.inventory.inventory_manager as inventory
import src.inventory.item as item

from src.lib.transform import Transform
from src.entity.player import Player
from src.entity.enemy import Enemy
from src.entity.spider import Spider
from src.entity.turret import Turret

# Create the shaders
player_light_shader = lighting.pixel_shader(500, (255, 245, 182), 1, False)
fire_shader = lighting.pixel_shader(500, (235, 89, 40), 0.75, False)
heart_shader = lighting.pixel_shader(500, (255, 0, 0), 0.5, False)
arctium_shader = lighting.pixel_shader(500, (9, 171, 235), 0.5, False)

class WorldScreen(ScreenBase):
    def __init__(self, world: str = "ruinMap"):
        ScreenBase.__init__(self)
        
        # Load the world data and store current world
        self.current_world = world
        world_data = json.load(open(f"worlds/{self.current_world}.json"))

        # Load the music
        mixer.music.load(world_data["music"])
        mixer.music.set_volume(0.1)
        mixer.music.play()   

        # Image paths for items to be displayed in the world
        self.pistol_img = "assets/sprites/items/pistol.png"
        self.merc_pistol_img = "assets/sprites/items/merc_pistol.png"
        self.arct_blaster_img = "assets/sprites/items/arct_blaster.png"
        self.ammo_img = "assets/sprites/items/ammo.png"
        self.heart_img = "assets/sprites/items/heart.png"
        self.arctium_img = "assets/sprites/items/arctium.png"

        # Set spawn locations based on the world data
        self.enemy_spawn_points = world_data["enemy_spawn_points"]
        self.arctium_spawn_points = world_data["arctium_spawn_points"]

        # Lists for enemies
        self.enemies: list[Enemy] = []
        self.turrets: list[Turret] = []

        # Spawn cooldowns for entities
        self.spawn_cooldown = world_data["spawn_cooldown"]
        self.spider_spawn = False
        self.arctium_spawn = False

        # Lists for items
        self.ammo: list[item.Item] = []
        self.hearts: list[item.Item] = []
        self.arctium: list[item.Item] = []

        # Populating hearts and arctium from world's json file
        for heart in world_data["hearts"]:
            self.hearts.append(item.Item(heart["x"], heart["y"], self.heart_img))

        for arctium in world_data["arctium"]:
            self.arctium.append(item.Item(arctium["x"], arctium["y"], self.arctium_img))

        # Add turrets to caveMap
        for turret in world_data["turrets"]:
            self.turrets.append(
                Turret(
                    Vector2(turret["x"], turret["y"]),
                    Vector2(turret["direction_x"], turret["direction_y"]),
                )
            )

        # Read player data
        self.player = Player(
            position=Vector2(world_data["player"]["x"], world_data["player"]["y"])
        )
        self.player.set_player()

        # Create pistol in ruinMap if player doesn't have one
        if (
            inventory.InventoryManager.getInstance().pistol_count == 0
            and world == "ruinMap"
        ):
            try:
                self.pistol = item.Weapon(
                    world_data["pistol"]["x"],
                    world_data["pistol"]["y"],
                    self.pistol_img,
                    world_data["pistol"]["damage"],
                    world_data["pistol"]["fire_rate"],
                )
            except:
                self.pistol = (
                    item.Weapon()
                )  # Set empty item if weapon properties are not defined
            self.render_pistol = True
        else:
            self.pistol = item.Weapon()
            self.render_pistol = False
        self.pistol.collected = False

        # Create merc pistol in ruinMap if player doesn't have one
        if (
            inventory.InventoryManager.getInstance().merc_pistol_count == 0
            and world == "ruinMap"
        ):
            try:
                self.merc_pistol = item.Weapon(
                    world_data["merc_pistol"]["x"],
                    world_data["merc_pistol"]["y"],
                    self.merc_pistol_img,
                    world_data["merc_pistol"]["damage"],
                    world_data["merc_pistol"]["fire_rate"],
                )
            except:
                self.merc_pistol = item.Weapon()
            self.render_merc = True
        else:
            self.merc_pistol = item.Weapon()
            self.render_merc = False

        # Create arct_blaster in caveMap if player doesn't have one
        if (
            inventory.InventoryManager.getInstance().arct_blaster_count == 0
            and world == "caveMap"
        ):
            try:
                self.arct_blaster = item.Weapon(
                    world_data["arct_blaster"]["x"],
                    world_data["arct_blaster"]["y"],
                    self.arct_blaster_img,
                    world_data["arct_blaster"]["damage"],
                    world_data["arct_blaster"]["fire_rate"],
                )
            except:
                self.arct_blaster = item.Weapon()
            self.render_blaster = True
        else:
            self.arct_blaster = item.Weapon()
            self.render_blaster = False

        # Assign empty pistols to player if uncollected
        if inventory.InventoryManager.getInstance().pistol_count == 0:
            self.player.pistol = self.pistol
            self.player.pistol.collected = False
        if inventory.InventoryManager.getInstance().merc_pistol_count == 0:
            self.player.merc_pistol = self.merc_pistol
            self.player.merc_pistol.collected = False
        if inventory.InventoryManager.getInstance().arct_blaster_count == 0:
            self.player.arct_blaster = self.arct_blaster
            self.player.arct_blaster.collected = False

        # Set strength of arct blaster
        self.player.arct_blaster.is_arctium = True

        # Create chest
        self.chest = item.Item(
            world_data["chest"]["x"],
            world_data["chest"]["y"],
            "assets/sprites/items/chest.png",
        )

        # Extracting all rect objects from the TileMap
        self.tilemap = tilemap.TiledMap(world_data["tilemap"])
        self.barriers = self.tilemap.get_rects_in_layer("Barriers")

        self.navmesh = Navmesh(
            (self.tilemap.width, self.tilemap.height), 32, self.tilemap, ("Barriers",)
        )

        # Fire objects
        self.fire: list[pygame.Rect] = self.tilemap.get_rects_in_layer("Fire")
        self.fire_lights: list[lighting.Light] = []

        # Setting lighting for objects
        self.player_light = lighting.Light(500, player_light_shader)

        for i in range(0, len(self.fire)):
            self.fire_lights.append(lighting.Light(500, fire_shader))

        for heart in self.hearts:
            heart.set_light(lighting.Light(500, heart_shader))

        for arctium in self.arctium:
            arctium.set_light(lighting.Light(500, arctium_shader))

        # Sound effects
        self.crawler_sound = pygame.mixer.Sound("assets/sounds/effects/crawler_death.wav")
        self.crawler_sound.set_volume(0.3)

        self.spider_sound = pygame.mixer.Sound("assets/sounds/effects/spider_death.wav")
        self.spider_sound.set_volume(0.3)

        # Get player position for lighting
        self.player_pos = self.player.get(Transform).pos
        self.px = self.player_pos[0]
        self.py = self.player_pos[1]

        # Create some enemies to start
        for x in range(5):
            self.start_spawn(self.spawn_enemy, self.enemy_spawn_points, False)

    def process_input(self, events: list):
        self.player.process_input(events)

        # Update inventory selection based on keyboard input (1-6)
        inventory.InventoryManager.getInstance().set_selected(events)

    def update(self):
        # Restart music if it's done playing
        if mixer.music.get_busy() == False:
            mixer.music.play()

        # Update turret and turret bullets
        for turret in self.turrets:
            turret.update(self.player)
            turret.update_bullets(self.barriers, self.player)

        # Update player
        self.player.move()
        self.player.update(
            self.barriers,
            self.enemies,
            self.turrets,
            self.pistol,
            self.merc_pistol,
            self.arct_blaster,
            self.ammo,
            self.hearts,
            self.arctium,
            self.chest,
        )

        # Update HUD information
        ui_elements.HUD.getInstance().update(self.player)

        # Update Cursor position
        ui_elements.Cursor.getInstance().update()

        for enemy in self.enemies:
            # Remove dead enemies
            if enemy.hp <= 0:
                # Play corresponding enemy death sound
                if enemy.is_spider:
                    pygame.mixer.Sound.play(self.spider_sound)
                else:
                    pygame.mixer.Sound.play(self.crawler_sound)
                self.enemies.remove(enemy)
                
                # Drop ammunition
                self.ammo.append(
                    item.Item(
                        enemy.get(Transform).pos.x,
                        enemy.get(Transform).pos.y,
                        self.ammo_img,
                    )
                )

                # Increase player stats
                self.player.maxHP *= 1.02  
                self.player.kills += 1 
            else:
                # Update pathfinding for alive enemies
                if self.navmesh.should_update():
                    threading.Thread(
                        target=self.update_enemy_nodes, args=(enemy,)
                    ).start()

                enemy.update()

        # Check for collected items to determine which to render
        if self.pistol.collected == True:
            self.render_pistol = False
        if self.merc_pistol.collected == True:
            self.merc_pistol.collected = True
            self.render_merc = False
        if self.arct_blaster.collected == True:
            self.arct_blaster.collected = True
            self.render_blaster = False
        for ammo in self.ammo:
            if ammo.collected == True:
                self.ammo.remove(ammo)
        for heart in self.hearts:
            if heart.collected == True:
                self.hearts.remove(heart)
        for arctium in self.arctium:
            if arctium.collected == True:
                self.arctium.remove(arctium)

        # Update Navmesh
        self.navmesh.update()

        # Check for level completion
        if self.chest.collected:
            mixer.music.stop()
            ui_elements.HUD.getInstance().dungeons += 1
            self.player.save_player_data()
            self.switch_to_scene(LevelClear(self.current_world))

        # Spawn crawlers
        if self.spawn_cooldown <= 0:
            self.start_spawn(self.spawn_enemy, self.enemy_spawn_points, False)
            self.spawn_cooldown = 100

            # Spawn spiders half as often as crawlers in cave
            if self.spider_spawn and self.current_world == "caveMap":
                self.start_spawn(self.spawn_enemy, self.enemy_spawn_points, True)

                # Spawn arctium crystals half as often as spiders in cave
                if self.arctium_spawn:
                    self.start_spawn(self.spawn_arctium, self.arctium_spawn_points)
                self.arctium_spawn = not self.arctium_spawn
            self.spider_spawn = not self.spider_spawn
        else:
            self.spawn_cooldown -= 1

        # If player died
        if self.player.currentHP <= 0:
            mixer.music.stop()

            # If player has < 10 ammo, refresh ammo
            if inventory.InventoryManager.getInstance().ammo_count < 10:
                inventory.InventoryManager.getInstance().ammo_count = 10
            
            # Save player's new stats
            self.player.save_player_data()
            self.switch_to_scene(GameOver(self.current_world))

    # Method to determine spawn areas for crawlers, spiders, and arctium crystals
    def start_spawn(self, spawn, spawn_points, is_spider=False):
        # Determine region of spawn (3 possible areas)
        spawn_area = random.randint(1, 6)

        # Least Spawn
        if spawn_area == 1:
            spawn(
                (
                    spawn_points["least"]["x_range"]["min"],
                    spawn_points["least"]["x_range"]["max"],
                ),
                (
                    spawn_points["least"]["y_range"]["min"],
                    spawn_points["least"]["y_range"]["max"],
                ),is_spider
            )

        # Average spawn
        elif spawn_area < 4:
            spawn(
                (
                    spawn_points["average"]["x_range"]["min"],
                    spawn_points["average"]["x_range"]["max"],
                ),
                (
                    spawn_points["average"]["y_range"]["min"],
                    spawn_points["average"]["y_range"]["max"],
                ),is_spider
            )

        # Most spawn
        else:
            spawn(
                (
                    spawn_points["most"]["x_range"]["min"],
                    spawn_points["most"]["x_range"]["max"],
                ),
                (
                    spawn_points["most"]["y_range"]["min"],
                    spawn_points["most"]["y_range"]["max"],
                ),is_spider
            )

    # Methods to spawn entities, using ranges from the start_spawn method
    def spawn_enemy(self, xRange, yRange, is_spider):
        position = Vector2(
            random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])
        )
        # Spawn crawler
        if not is_spider:
            self.enemies.append(Enemy(position, 100, 1, False))
        # Spawn spider
        else:
            self.enemies.append(Enemy(position, 50, 4, True))
    def spawn_arctium(self, xRange, yRange, none):
        position = Vector2(
            random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])
        )
        
        # Setting lighting for newly spawned crystals
        temp = item.Item(position.x, position.y, self.arctium_img)
        temp.set_light(lighting.Light(500, arctium_shader))
        self.arctium.append(temp)

    # Updating pathfinding for enemies
    def update_enemy_nodes(self, enemy: Enemy):
        enemy.set_nodes(
            a_star.algorithm(
                self.navmesh.nodes,
                enemy.get(Transform).pos,
                self.player.get(Transform).pos,
            )
        )

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))

        # Render map
        self.tilemap.render(screen)

        # Render player
        self.player.render(screen)

        # Render enemies
        for enemy in self.enemies:
            enemy.render(screen)

        # Render turrets
        for turret in self.turrets:
            turret.render(screen)

        # Render uncollected items
        if self.render_pistol == True:
            self.pistol.render(screen)
        if self.render_merc == True:
            self.merc_pistol.render(screen)
        if self.render_blaster == True:
            self.arct_blaster.render(screen)
        for ammo in self.ammo:
            ammo.render(screen)
        for heart in self.hearts:
            heart.render(screen)
        for arctium in self.arctium:
            arctium.render(screen)

        # Render chest
        self.chest.render(screen)

        # Get player position for lighting
        self.player_pos = self.player.get(Transform).pos
        self.px = self.player_pos[0]
        self.py = self.player_pos[1]

        # Render the light
        lights_display = pygame.Surface((screen.get_size()))
        lights_display.blit(lighting.global_light(screen.get_size(), 50), (0, 0))

        for i in range(0, len(self.fire)):
            self.fire_lights[i].main(
                self.barriers,
                lights_display,
                self.fire[i].centerx,
                self.fire[i].centery,
            )

        for heart in self.hearts:
            heart.get_light().main(self.barriers, lights_display, heart.x, heart.y)

        for arctium in self.arctium:
            arctium.get_light().main(
                self.barriers, lights_display, arctium.x, arctium.y
            )

        self.player_light.main(self.barriers, lights_display, self.px, self.py)

        screen.blit(lights_display, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

        # Render the HUD
        ui_elements.HUD.getInstance().render(screen)

        # Render the custom cursor
        ui_elements.Cursor.getInstance().render(screen)

    def switch_to_scene(self, next_scene):
        self.next = next_scene