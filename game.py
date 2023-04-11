import pygame
import screens.screen_base as screen_base
import screens.start_screens as start_screens
from pygame.locals import *

import src.ui.ui_elements as ui_elements
from src.inventory.inventory_manager import InventoryManager

# Initialize pygame for the current OS
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Create the icon image
icon = pygame.image.load("assets/icon.png")
pygame.display.set_caption("Ruin Raider")
pygame.display.set_icon(icon)

# Main game loop
def run_game(
    width: int, height: int, fps: int, starting_scene: screen_base.ScreenBase
) -> None:
    """Runs the game with the given a starting scene and dimension."""
    pygame.init()
    screen = pygame.display.set_mode((width, height), DOUBLEBUF)
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    active_scene = starting_scene
    InventoryManager.getInstance().set_sound()

    while active_scene != None:
        clock.tick(fps)
        ui_elements.HUD.getInstance().fps = clock.get_fps()

        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                # Alt key tracking for Alt-F4 functionality
                alt_pressed = event.key == pygame.K_LALT or event.key == pygame.K_RALT
                if event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True

            if quit_attempt:
                active_scene.terminate()
            else:
                filtered_events.append(event)

        active_scene.process_input(filtered_events)
        active_scene.update()
        active_scene.render(screen)

        active_scene = active_scene.next

        pygame.display.update()

# Run game TODO: change back to splash screen upon submission
run_game(1216, 832, 60, start_screens.SplashScreen())