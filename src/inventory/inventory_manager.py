import pygame

# Class to manage player inventory
class InventoryManager:
    __instance = None

    # Static instance for global access
    @staticmethod
    def getInstance():
        """Static access method."""
        if InventoryManager.__instance == None:
            InventoryManager.__instance = InventoryManager()
        return InventoryManager.__instance

    def __init__(self):
        """Virtually private constructor."""
        if InventoryManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            InventoryManager.__instance = self
            self.pistol_count = 0
            self.merc_pistol_count = 0
            self.arct_blaster_count = 0
            self.ammo_count = 10 # Starting ammo count
            self.heart_count = 0
            self.arctium_count = 0
            self.chest_count = 0
            self.selected = 1

    # Set sound effects    
    def set_sound(self):
        self.select_sound = pygame.mixer.Sound("assets/sounds/effects/glass_006.ogg")
        self.select_sound.set_volume(0.15) 
    
    # Set the selected inventory slot depending on keyboard input
    def set_selected(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or
                    event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6):
                    pygame.mixer.Sound.play(self.select_sound)
                    if event.key == pygame.K_1:
                        self.selected = 1
                    elif event.key == pygame.K_2:
                        self.selected = 2
                    elif event.key == pygame.K_3:
                        self.selected = 3
                    elif event.key == pygame.K_4:
                        self.selected = 4
                    elif event.key == pygame.K_5:
                        self.selected = 5
                    elif event.key == pygame.K_6:
                        self.selected = 6
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5: # Mouse scroll up
                    if self.selected == 6:
                        self.selected = 1
                    else:
                        self.selected += 1
                    pygame.mixer.Sound.play(self.select_sound)
                elif event.button == 4: # Mouse scroll down
                    if self.selected == 1:
                        self.selected = 6
                    else:
                        self.selected -=1
                    pygame.mixer.Sound.play(self.select_sound)

    # Return the count of an item in a particular slot
    def get_count(self, slot_num):
        if slot_num == 1:
            return self.pistol_count
        elif slot_num == 2:
            return self.merc_pistol_count
        elif slot_num == 3:
            return self.arct_blaster_count
        elif slot_num == 4:
            return self.ammo_count
        elif slot_num == 5:
            return self.heart_count
        elif slot_num == 6:
            return self.arctium_count
    
    # Detect item use (mouse click) when a slot is selected
    def is_used(self, selection, events):
        if self.selected == selection and self.get_count(selection) > 0:
            for event in events:
                if (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]) or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    return True
        return False