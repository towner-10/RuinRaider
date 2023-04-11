import src.inventory.inventory_manager as inventory

# Test inventory checks for pistol
def test_pistol():
        
    # Define ammo count test cases
    ammo_counts = [4, 1, 0]

    # Test each ammo count
    for ammo in ammo_counts:
        shoot = False
        inventory.InventoryManager.getInstance().ammo_count = ammo

        # Imported if statement from player method
        if inventory.InventoryManager.getInstance().get_count(4) > 0:
            #pygame.mixer.Sound.play(self.pistol_sound)
            #self.pistol.shoot(Vector2.copy(self.get(Transform).pos), self.get(Transform).angle)
            inventory.InventoryManager.getInstance().ammo_count -= 1
            shoot = True

        # Check if shot if ammo is > 0
        if ammo > 0:
            # Check if ammo count updated properly
            assert inventory.InventoryManager.getInstance().get_count(4) == ammo - 1
 
            assert shoot
        else:
            # Check if ammo remained unchanged and no shots fired
            assert inventory.InventoryManager.getInstance().get_count(4) == ammo
            assert not shoot
        
# Test inventory checks for merc pistol
def test_merc():
        
    # Define ammo count test cases
    ammo_counts = [7, 5, 3]

    # Test each ammo count
    for ammo in ammo_counts:
        shoot = False
        inventory.InventoryManager.getInstance().ammo_count = ammo

        # Imported if statement from player method
        if inventory.InventoryManager.getInstance().get_count(4) - 5 >= 0:
            #pygame.mixer.Sound.play(self.merc_pistol_sound)
            #self.merc_pistol.shoot(Vector2.copy(self.get(Transform).pos), self.get(Transform).angle)
            inventory.InventoryManager.getInstance().ammo_count -= 5
            shoot = True

        # Check if shot if ammo is >= 5
        if ammo >= 5:
            # Check if ammo count updated properly
            assert inventory.InventoryManager.getInstance().get_count(4) == ammo - 5

            assert shoot
        else:
            # Check if ammo remained unchanged and no shots fired
            assert inventory.InventoryManager.getInstance().get_count(4) == ammo
            assert not shoot

# Test inventory checks for arct blaster
def test_blaster():
        
    # Define arctium count test cases
    arctium_counts = [4, 1, 0]

    # Test each arctium count
    for arctium in arctium_counts:
        shoot = False
        inventory.InventoryManager.getInstance().arctium_count = arctium

        # Imported if statement from player method
        if inventory.InventoryManager.getInstance().get_count(6) > 0:
            #pygame.mixer.Sound.play(self.arct_blaster_sound)
            #self.arct_blaster.shoot(Vector2.copy(self.get(Transform).pos), self.get(Transform).angle)
            inventory.InventoryManager.getInstance().arctium_count -= 1
            shoot = True

        # Check if shot if arctium is >= 5
        if arctium > 0:
            # Check if arctium count updated properly
            assert inventory.InventoryManager.getInstance().get_count(6) == arctium - 1

            assert shoot
        else:
            # Check if arctium remained unchanged and no shots fired
            assert inventory.InventoryManager.getInstance().get_count(6) == arctium
            assert not shoot

# Test inventory checks for ammo crafting
def test_ammo():
    # Define ammo count test cases
    ammo_counts = [23, 20, 17]

    # Test each ammo count
    for ammo in ammo_counts:
        craft = False
        inventory.InventoryManager.getInstance().ammo_count = ammo
        inventory.InventoryManager.getInstance().heart_count = 0

        # Imported if statement from player method
        if inventory.InventoryManager.getInstance().get_count(4) - 20 >= 0:
            #pygame.mixer.Sound.play(self.craft_sound)
            inventory.InventoryManager.getInstance().ammo_count -= 20
            inventory.InventoryManager.getInstance().heart_count += 1
            craft = True

        # Check if crafted if ammo is >= 20
        if ammo >= 20:
            # Check if ammo count updated properly
            assert inventory.InventoryManager.getInstance().get_count(4) == ammo - 20

            # Check if heart count updated properly
            assert inventory.InventoryManager.getInstance().get_count(5) == 1

            assert craft
        else:
            # Check if ammo/hearts remained unchanged and no craft
            assert inventory.InventoryManager.getInstance().get_count(4) == ammo
            assert inventory.InventoryManager.getInstance().get_count(5) == 0
            assert not craft

# Test inventory checks for heart usage
def test_heart():
    # Define hp amount test cases
    hp_amounts = [100, 90, 80, 60]
    max_hp = 100

    # Test each hp amount
    for hp in hp_amounts:
        current_hp = hp
        inventory.InventoryManager.getInstance().heart_count = 1

        # Imported if statement from player method
        if max_hp > current_hp:
            if current_hp + max_hp // 5 > max_hp:
                current_hp = max_hp
            else:
                current_hp += max_hp // 5
                #pygame.mixer.Sound.play(self.heal_sound)
            inventory.InventoryManager.getInstance().heart_count -= 1

        # Check if healed
        if max_hp > hp:
            # Check if heart count updated properly
            assert inventory.InventoryManager.getInstance().get_count(5) == 0

            # Check hp
            if hp + max_hp // 5 > max_hp:
                assert current_hp == max_hp
            else:
                assert current_hp == hp + max_hp // 5
        else:
            # Check if heart count/hp remained unchanged
            assert inventory.InventoryManager.getInstance().get_count(5) == 1
            assert current_hp == hp 

# Test inventory checks for arctium crafting
def test_arctium():
    # Define arctium count test cases
    arctium_counts = [4, 1, 0]

    # Test each arctium count
    for arctium in arctium_counts:
        craft = False
        inventory.InventoryManager.getInstance().arctium_count = arctium
        inventory.InventoryManager.getInstance().ammo_count = 0

        # Imported if statement from player method
        if inventory.InventoryManager.getInstance().get_count(6) - 1 >= 0:
            #pygame.mixer.Sound.play(self.craft_sound)
            inventory.InventoryManager.getInstance().arctium_count -= 1
            inventory.InventoryManager.getInstance().ammo_count += 10
            craft = True

        # Check if crafted if arctium is > 0
        if arctium > 0:
            # Check if arctium count updated properly
            assert inventory.InventoryManager.getInstance().get_count(6) == arctium - 1

            # Check if ammo count updated properly
            assert inventory.InventoryManager.getInstance().get_count(4) == 10

            assert craft
        else:
            # Check if arctium/ammo remained unchanged and no craft
            assert inventory.InventoryManager.getInstance().get_count(6) == arctium
            assert inventory.InventoryManager.getInstance().get_count(4) == 0
            assert not craft