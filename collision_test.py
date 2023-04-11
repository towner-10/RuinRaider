import json
import pygame
import src.ui.ui_elements as ui_elements
from pygame import Vector2
from src.entity.player import Player
import src.lib.tilemap as tilemap
from src.lib.transform import Transform

def barrier_collision():
    pygame.mixer.init()
    screen = pygame.display.set_mode((1216,832))
    world_data = json.load(open(f"worlds/ruinMap.json"))
    tm = tilemap.TiledMap(world_data["tilemap"])
    barriers = tm.get_rects_in_layer("Barriers")
    
    player = Player(
        position=Vector2(world_data["player"]["x"], world_data["player"]["y"])
    )
    player.set_player()
    player.moving = True
    player.direction.x = player.speed
        
    for x in range(500):
        player.move()
        player.update_player(
            barriers
            )

    assert player.moving == False
    assert player.get(Transform).pos == [688, 576]

barrier_collision()