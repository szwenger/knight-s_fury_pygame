#--- To Do List ---
#--> status
#paths anpassen
#rescale Resolution fix --> rescale Original image
#rescale hitboxes
#player position + velocity


# ---------- Import Modules and Libaries ----------

import pygame, random, math, time
from constants import * # Import all variables from variables.py
from main_menu import MainMenu
from start_screen import Start_Screen
from options import Options
from death_screen import Death_Screen
from cursor import Cursor
from player import Player
from arrow import Arrow
from enemy import *
from field import Field
from sidemenu import SideMenu
#from debug import debug


pygame.init() # Initialize Pygame

# ---------- Set Game Icon and Title ----------

pygame.display.set_caption("Knight's Fury") # Set the window title
pygame.display.set_icon(game_icon) # Set the window icon

# ---------- Screen ----------
global screen_width, screen_height
screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height),pygame.RESIZABLE) # Set the screen size

pygame.mouse.set_visible(False) # Hide the mouse cursor

# ---------- Functions ----------

drawn = [] # for archer arrows

def update_all_for_resize(old_screen_width, old_screen_height, snowflakes: list):
    global screen_width, screen_height
    screen_width = old_screen_width
    screen_height = old_screen_height
    # Import all variables from variables.py
    # Get new screen size
    (new_screen_width, new_screen_height) = event.size

    # Keep 16:9 aspect ratio
    # Calculate the aspect ratio dimensions
    min_screenside = min(new_screen_width, new_screen_height * (16/9))

    # Calculate new screen size
    if min_screenside < 144:
        new_screen_width = 192
        new_screen_height = 144
        print("Screen too small")
    else:
        new_screen_width = int(round(min_screenside))
        new_screen_height = int(round(min_screenside * (9/16)))
        print("Screen resized to: ", new_screen_width, new_screen_height)

    # Set the screen size if it's different from the current size
    if new_screen_width != screen_width or new_screen_height != screen_height:
        screen = pygame.display.set_mode((new_screen_width, new_screen_height), pygame.RESIZABLE)
        screen_width = new_screen_width
        screen_height = new_screen_height

    main_menu.update_for_resize(screen_width, screen_height)
    cursor.update_for_resize(screen_height)

    # Update field and sidemenu size
    old_fieldlength = field.sidelength
    field.update_for_resize(screen_height)
    new_fieldlength = field.sidelength

    start_screen.update_for_resize(screen_width, screen_height, snowflakes)
    sidemenu.update_for_resize(screen_width, screen_height)
    death_screen.update_for_resize(new_fieldlength)
    cursor.update_for_resize(screen_height)

    # Update player and enemy size and position
    player.update_for_resize(old_fieldlength, new_fieldlength)

    # Update enemy position and speed
    for enemy in enemies:
        enemy.update_for_resize(field, old_fieldlength, screen_width)
        if isinstance(enemy, archer):
            for enemy_arrow in enemy.arrows:
                enemy_arrows.update_for_resize(field.sidelength)

    for i in range(0, 9, 1):
        sword_sprites[i] = pygame.transform.scale(sword_sprites[i], (player.size[0] * (5/2), player.size[1] * (5/2)))

    options.update_for_resize(screen_width, screen_height, snowflakes)

    for player_arrow in player.arrows:
        player_arrow.update_for_resize(field.sidelength)

    old_screen_width = screen_width
    old_screen_height = screen_height

# Function to rotate an image to a target position   
def rotate_image(source_pos, target_pos, image):
    # Calculate the angle between the source and the target
    source_pos_vector = pygame.math.Vector2(source_pos)
    target_pos_vector = pygame.math.Vector2(target_pos)
    direction = target_pos_vector - source_pos_vector
    angle = math.degrees(math.atan2(-direction.y, direction.x))

    # Create a new surface with the same dimensions as the original image
    image_rotated = pygame.Surface(image.get_size(), pygame.SRCALPHA)

    # Rotate the image
    rotated_image = pygame.transform.rotate(image, angle)

    # Blit the rotated image onto the new surface, centered
    rect = rotated_image.get_rect(center=image_rotated.get_rect().center)
    image_rotated.blit(rotated_image, rect)

    return image_rotated

snowflakes = []
for _ in range(100):  # Create 100 snowflakes
    flake = {
        'x': random.randint(0, screen_width),  # Random x-coordinate
        'y': random.randint(0, screen_height),  # Random y-coordinate
        'size': random.randint(1, 3),  # Random size
        'speed': random.randint(1, 3),  # Random speed
    }
    snowflakes.append(flake)

# ---------- Waves ----------

wave = 1
enemycount = 3
score = 0

# ---------- Create Objects ----------

start_screen = Start_Screen(screen, screen_width, screen_height) # Create Start Screen Object
main_menu = MainMenu(screen_width, screen_height) # Create MainMenu Object
cursor = Cursor() # Create Cursor Object

field = Field() # Create Field Object
sidemenu = SideMenu(screen_width, screen_height) # Create SideMenu Object

enemies = [SmallGoblin(field)for i in range(enemycount)]  #Create list of enemies

#enemies = [archer(field), Orc(field), Ogre(field), SmallGoblin(field)]
player = Player(field) # Create Player Object

death_screen = Death_Screen(screen, player, field) # Create Death Screen Object
options = Options(screen, screen_width, screen_height) # Create Options Object

# ---------- Load Textures ----------

for i in range (0, 9, 1):
    sword_sprites[i] = pygame.transform.scale(sword_sprites[i], (player.size[0]*(5/2), player.size[1]*(5/2)))
# field_image = field.load_background(background_1_img) # Load Background Image
# player_texture = player.load_texture(player_still_img) # Load Player Image

# ---------- Main Loop ----------
f = open(get_path("_resources", "highscore.txt"), "r")
highscore = max(int(line.strip()) for line in f.readlines()) #Aktueller Highscore
f.close()

opened_game = pygame.time.get_ticks()
run = True
global status
status = "start_screen"

while run:
    # Limit frame rate
    pygame.time.Clock().tick(FPS)
    
    if status == "start_screen":
        start_screen.draw(screen, snowflakes, opened_game, pygame.time.get_ticks()) # Draw Start Screen
        cursor.draw(screen)
        
        # Music
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.load(get_path("_sounds", "Minifantasy_Dungeon_Music", "Music", "Goblins_Den_(Regular).wav"))
            pygame.mixer.music.play(-1)
        
        # --- Event handler - Start Screen ---
        
        old_screen_width = screen_width
        old_screen_height = screen_height
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                update_all_for_resize(old_screen_width, old_screen_height, snowflakes)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_screen.rect.collidepoint(event.pos):
                    status = "mainmenu"
            
            # Quit Game
            if event.type == pygame.QUIT:
                run = False
        
        if pygame.time.get_ticks() - opened_game > 10000:
            status = "mainmenu"
    
    if status == "mainmenu":
        menu_shown = pygame.time.get_ticks()
        # Draw Main Menu
        main_menu.draw(screen, menu_shown, opened_game) # Draw Main Menu
        cursor.draw(screen)
        
        # Music
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.load(get_path("_sounds", "Minifantasy_Dungeon_Music", "Music", "Goblins_Den_(Regular).wav"))
            pygame.mixer.music.play(-1)
        
        # --- Event handler - Main Menu ---
        
        old_screen_width = screen_width
        old_screen_height = screen_height
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                update_all_for_resize(old_screen_width, old_screen_height, snowflakes)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu.start_rect.collidepoint(event.pos):
                    started_game_from_mainmenu = True
                    start_time = time.time()
                    last_update = pygame.time.get_ticks()
                    pygame.mixer.music.fadeout(1000)
                    status = "running"
                elif main_menu.options_rect.collidepoint(event.pos):
                    status = "options"
                elif main_menu.quit_rect.collidepoint(event.pos):
                    run = False
            
            # Quit Game
            if event.type == pygame.QUIT:
                run = False
   
    if status == "running":
        
        current_time = pygame.time.get_ticks()
        
        # Music
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.load(get_path("_sounds", "Minifantasy_Dungeon_Music", "Music", "Goblins_Dance_(Battle).wav"))
            pygame.mixer.music.play(-1)
        
        #Waves 
        if player.health <= 0:
            f = open(get_path("_resources", "highscore.txt"), "a")
            f.write(str(score) + "\n")
            f.close()
            print("You Died.")
            print(f"Score: {player.kills * wave}")
            pygame.image.save(screen, get_path("_images", "before_death_screen.png"))
            death_screen.background = pygame.image.load(get_path("_images", "before_death_screen.png"))
            status = "death_screen"
            
        if player.kills >= 999:
            print("You Win!")
            run = False
            
        if len(enemies) == 0: #Check if all enemies are defeated
            print("Wave", wave)
            enemies = [SmallGoblin(field)for i in range(round((enemycount/2))*wave)]+ [Orc(field)for i in range(wave)]
            if wave == 0:
                enemies = [SmallGoblin(field)for i in range(enemycount)]
            if wave % 5 == 0:
                enemies = enemies + [Ogre(field)for i in range(round(wave/2))]
            if wave >= 5:
                player.health = 2
            if wave == 3:
                enemies.append(Ogre(field))
            if wave > 3: 
                enemies = enemies + [archer(field)for i in range(round(wave/2))]
            wave +=1 #Increase wave count
            enemycount += 1 #Increase enemy count
            
                
        key = pygame.key.get_pressed()
        
        old_screen_width = screen_width
        old_screen_height = screen_height
        
        
        for event in pygame.event.get():
            # Resize Window Event
            if event.type == pygame.VIDEORESIZE:
                update_all_for_resize(old_screen_width, old_screen_height, snowflakes)
                
            # Quit Game - Close Window
            if event.type == pygame.QUIT:
                run = False
            
            # Spawn and remove enemies for testing - I and O
            elif event.type == pygame.KEYDOWN:  # Ein Tastendruck-Ereignis
                if event.key == pygame.K_i:  # Die Taste "i" wurde gedrückt
                    if enemies:  # Überprüft, ob die Liste nicht leer ist
                        enemies.pop(0)  # Entfernt das erste Element aus der Liste

                elif event.key == pygame.K_o:  # Die Taste "o" wurde gedrückt
                    enemies.append(SmallGoblin(field))  # Fügt einen neuen Feind zur Liste hinzu
                    enemies.append(SmallGoblin(field))  # Fügt einen weiteren neuen Feind zur Liste hinzu
                    enemies.append(Orc(field))  # Fügt einen weiteren neuen Feind zur Liste hinzu
                
                elif event.key == pygame.K_ESCAPE:
                    status = "mainmenu"

            # Attack - Left Mouse Button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if player.last_hit + 500 < current_time:
                        player.attacking = True
                elif event.button == 3:
                    if player.last_hit + 500 < current_time:
                        if player.arrowcount >0:
                            player.arrowcount -=1
                            angle = player.calculate_angle(cursor.get_position())
                            arrow_current_image = rotate_image(player.middle, cursor.get_position(), arrow_img)
                            shot_arrow = Arrow(player.middle[0], player.middle[1], angle, 10, 1, arrow_current_image, field)
                            player.arrows.append(shot_arrow)
                        else:
                            print("Out of Arrows!")
                    player.last_hit = pygame.time.get_ticks()

        
        # --- Main Game Logic ---
        
        field.draw(screen) # Draw Background
        player.move(field) # Move Player
        
        # Check if player is moving
        if player.position != player.last_position:
            player.moving = True
        else:
            player.moving = False
        
        player.last_position = player.position

        # Rotate the image
        def rotate_image_attack_animation(image, angle):
            return pygame.transform.rotate(image, angle + 180)

        # Attack Animation
        if player.attacking:
            # Calculate the angle between the player and the cursor
            angle = player.calculate_angle(cursor.get_position())

            # Rotate the image
            rotated_image = rotate_image_attack_animation(sword_sprites[player.attack_frame], angle)

            # Display the image
            screen.blit(rotated_image, (round(player.rect.topleft[0] - player.size[0]), round(player.rect.topleft[1] - player.size[1])))
            
            # Check for enemy collision
            if player.attack_frame == 4:
                hit_enemy_indices = player.check_hit(screen, enemies)  
                for idx in reversed(hit_enemy_indices):
                    sword_hit_sound = random.choice(player_sword_hit)
                    sword_hit_sound.play()
                    enemies[idx].health -= 1
                    if enemies[idx].health <= 0:
                        if enemies[idx].__class__ == archer:
                            player.arrowcount += 3
                        enemies.pop(idx)
                        player.kills += 1
                        score = player.kills*wave
                        print("Kills: ", player.kills)
                if not hit_enemy_indices:  # If the list is empty, no enemies were hit
                    missed_enemy = random.choice(player_sword_miss)
                    missed_enemy.play()
                print("Player Attack")
                player.attacking = True
                player.last_hit = pygame.time.get_ticks()

            # Update the attack frame
            player.attack_frame += 1

            # Reset the attack frame and stop attacking after the last frame
            if player.attack_frame == 9:
                player.attack_frame = 0
                player.attacking = False
                
        # Arrow Movement
        for arrow in player.arrows:
            arrow.move()
            arrow.draw(screen)
            if arrow.checkOffScreen(field.sidelength):
                player.arrows.remove(arrow)
            for enemy in enemies:
                if arrow.check_Collision_enemy(enemy):
                    player.arrows.remove(arrow)
                    # if enemy.__class__ == archer:
                    #     player.arrowcount += 3
                    if enemy.health >= 0:
                        enemy.health -= 1
                        if enemy.health <= 0:
                            enemies.remove(enemy)
                            player.kills += 1
                            score = player.kills * wave
                            print("Kills: ", player.kills)
                    
        
        # Player Moving Animation
        if player.moving == True:
            if current_time - last_update >= animation_cooldown:
                frame += 1
                if frame >= len(knight_sprites):
                    frame = 0
                last_update = current_time            
            player_img = knight_sprites[frame]
        else:
            player_img = knight_still_sprite                
        
        # Enemy Object
        for enemy in enemies:
            enemy.update((player.x, player.y), player.rect, enemy.speed, enemies) # Update the enemy position

            ###
            if enemy.__class__ == archer:
                if enemy.is_attacking:
                    if current_time - enemy.last_attack_time > enemy.delay:
                        enemy.last_attack_time = pygame.time.get_ticks()
                        angle = enemy.calculate_angle_to_player(player.middle)
                        arrow_current_image = rotate_image(enemy.middle, player.middle, arrow_img)
                        shot_arrow = Arrow(enemy.middle[0], enemy.middle[1], angle, 10, 1, arrow_current_image, field)
                        enemy.arrows.append(shot_arrow)
                        if enemy.inAttackRange(player.middle) == False:
                            enemy.arrows.clear()
                            enemy.arrows = drawn
                            enemy.is_attacking = False
                            
                    drawn = []
                for arrow in enemy.arrows:
                    arrow.move()
                    arrow.draw(screen)
                    drawn.append(arrow)
                    if arrow.checkOffScreen(field.sidelength):
                        enemy.arrows.remove(arrow)
                        drawn.remove(arrow)
                    if arrow.check_Collision_enemy(player):
                        enemy.arrows.remove(arrow)
                        drawn.remove(arrow)
                        player.health -= 1
                        print("Kills: ", player.kills)


            if enemy.hitplayer:
                player_damage_sound = random.choice(player_damage)
                player_damage_sound.play()
                player.health -= 1
                enemy.hitplayer = False


            if enemy.__class__ != Orc and enemy.__class__ != archer and enemy.__class__ != Ogre:
                # Skalieren Sie das Bild des Gegners entsprechend der neuen Größe des Rechtecks
                enemy_goblin_img_scaled = pygame.transform.scale(enemy_goblin_img, enemy.size)

                # Rotate the enemy image to the player position
                enemy_goblin_img_rotated = rotate_image(enemy.middle, player.middle, enemy_goblin_img_scaled)

                # Draw Enemy Model
                screen.blit(enemy_goblin_img_rotated, (round(enemy.x), round(enemy.y)))
            if enemy.__class__ == Orc:
                # Skalieren Sie das Bild des Gegners entsprechend der neuen Größe des Rechtecks
                orc_img_scaled = pygame.transform.scale(orc_img, enemy.size)

                # Rotate the enemy image to the player position
                orc_img_rotated = rotate_image(enemy.middle, player.middle, orc_img_scaled)

                # Draw Enemy Model
                screen.blit(orc_img_rotated, (round(enemy.x), round(enemy.y)))
            if enemy.__class__ == archer:
                # Skalieren Sie das Bild des Gegners entsprechend der neuen Größe des Rechtecks
                archer_img_scaled = pygame.transform.scale(archer_img, enemy.size)

                # Rotate the enemy image to the player position
                archer_img_rotated = rotate_image(enemy.middle, player.middle, archer_img_scaled)

                # Draw Enemy Model
                screen.blit(archer_img_rotated, (round(enemy.x), round(enemy.y)))
            
            if enemy.__class__ == Ogre:
                # Skalieren Sie das Bild des Gegners entsprechend der neuen Größe des Rechtecks
                ogre_img_scaled = pygame.transform.scale(ogre_img, enemy.size)

                # Rotate the enemy image to the player position
                ogre_img_rotated = rotate_image(enemy.middle, player.middle, ogre_img_scaled)

                # Draw Enemy Model
                screen.blit(ogre_img_rotated, (round(enemy.x), round(enemy.y)))
        
        mouse_pos = cursor.get_position()
        
        # Rotate the player image to the mouse position
        player_img_rotated = rotate_image(player.middle, mouse_pos, player_img)

        # Draw Player Model
        player.draw(screen, player_img_rotated)

        # Sidebar Information Screen
        sidemenu.draw(screen)
        sidemenu.draw_info(screen, player.health, player.kills, int(round(time.time()-start_time)), player.arrowcount, wave, score, highscore)
        
        # Draw Cursor
        cursor.draw(screen)
    
    if status == "death_screen":
        # Draw Death Screen
        death_screen.draw(enemies)
        wave = 0
        cursor.draw(screen)
        # --- Event handler - Death Screen ---
        
        for event in pygame.event.get():
            old_screen_height = screen_height
            old_screen_width = screen_width
            if event.type == pygame.VIDEORESIZE:
                update_all_for_resize(old_screen_width, old_screen_height, snowflakes)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if death_screen.restart_button.collidepoint(event.pos):
                    enemycount = 3
                    player.arrowcount = 0
                    player.kills = 0
                    player.health = 1
                    score = 0
                    start_time = time.time()
                    status = "running"
                elif death_screen.main_menu_button.collidepoint(event.pos):
                    status = "mainmenu"
                elif death_screen.quit_button.collidepoint(event.pos):
                    run = False
            # Quit Game
            if event.type == pygame.QUIT:
                run = False
    
    if status == "options":
        # Draw Options
        options.draw(screen, snowflakes)
        cursor.draw(screen)
        
        # --- Event handler - Options ---
        old_screen_height = screen_height
        old_screen_width = screen_width        
        for event in pygame.event.get():
            
            # Resize Window Event
            if event.type == pygame.VIDEORESIZE:
                update_all_for_resize(old_screen_width, old_screen_height, snowflakes)
            
            # Button Selection
            if event.type == pygame.MOUSEBUTTONDOWN:
                if options.back_button.collidepoint(event.pos):
                    status = "mainmenu"
                if options.music_button.collidepoint(event.pos):
                    if pygame.mixer.music.get_volume() == 0:
                        pygame.mixer.music.set_volume(0.5)
                        options.music_button_text = "Music: On"
                    else:
                        pygame.mixer.music.set_volume(0)
                        options.music_button_text = "Music: Off"
                if options.sound_button.collidepoint(event.pos):
                    sound_lists = [player_sword_miss, player_sword_hit, player_damage]
                    volume = 0 if player_sword_miss[0].get_volume() != 0 else 0.5
                    if volume == 0:
                        options.sound_button_text = "Sound: Off"
                    if volume == 0.5:
                        options.sound_button_text = "Sound: On"
                    for sound_list in sound_lists:
                        for sound in sound_list:
                            sound.set_volume(volume)
                
            # Quit Game
            if event.type == pygame.QUIT:
                run = False
    
    pygame.display.flip() #refresh screen
pygame.quit()

print("Game Closed")

