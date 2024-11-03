'''
Einfürung in die Programmierung - Praktikum 
Simon Zwenger, Max Schubert 

Resources:
Side Menu Scroll: https://www.kindpng.com/imgv/TiRwRmo_pixel-art-paper-scroll-transparent-hd-png-download/
Table Texture: https://itch.io/t/1452767/pixel-tutorial-wood-texture 
'''
# Import Modules and Libaries
import pygame, random, math, time
from variabes import * # Import all variables from variabes.py
from debug import debug

pygame.init() # Initialize Pygame

pygame.display.set_caption("KNIGHT(ingale)") # Set the window title
pygame.display.set_icon(game_icon) # Set the window icon

screen = pygame.display.set_mode((screen_width, screen_height),pygame.RESIZABLE) # Set the screen size

# Enemy Class
class Enemy:
    def __init__(self):
        # Initialisiere die x- und y-Koordinaten des Feindes zufällig
        spawn = random.randint(1,4) # Random Spawn
        if spawn == 1: #Oben
            self.x = 1*random.randint(0,screen_width)
            self.y = -1*random.randint(0,int(round(0.2 * screen_height)))
        elif spawn == 2: #Unten
            self.x = 1*random.randint(0,screen_width)
            self.y = 1*(random.randint(0,int(round(0.2 * screen_height)))+screen_height) 
        elif spawn == 3:#links
            self.x = -1*random.randint(0,int(round(0.2 * screen_width))) 
            self.y = 1*random.randint(0,screen_height)
        elif spawn == 4: #rechts
            self.x = 1*(random.randint(screen_height,int(round(screen_height + 0.2 * screen_height))))
            self.y = 1*random.randint(0,screen_height)
        
        self.rect  =pygame.Rect((self.x, self.y, int(round((5/108) * screen_height)),int(round((3/108) * screen_height))))  # Erstelle das Rechteck für den Feind

    def get_direction(self, player_pos):
        dx = player_pos[0] - self.x  # Berechne den x-Abstand zum Spieler
        dy = player_pos[1] - self.y  # Berechne den y-Abstand zum Spieler
        distance = math.sqrt(dx**2+dy**2)  # Berechne die Entfernung zum Spieler
        direction_x = dx / distance  # Normalisiere den x-Abstand
        direction_y = dy / distance  # Normalisiere den y-Abstand
        return direction_x, direction_y  # Gebe die Richtung zum Spieler zurück
    
    def collided(self, enemies):
        for enemy in enemies:
            if enemy is not self and self.rect.colliderect(enemy.rect):
                return True
        return False
    def enemycollide(self, enemies):
        for other_enemy in enemies:
            if self is not other_enemy and self.rect.colliderect(other_enemy.rect):
                # Calculate the direction to move the enemy away
                dx = self.x - other_enemy.x
                dy = self.y - other_enemy.y
                distance = math.sqrt(dx**2 + dy**2)

                # Move the enemy away a little bit
                self.x += dx / distance
                self.y += dy / distance

                # Update the rect property of the enemy after the position change
                self.rect.topleft = (round(self.x), round(self.y))

    def update(self, player_pos, speed, enemies):
        direction_x, direction_y = self.get_direction(player_pos)  # Get the direction to the player

        self.x += direction_x * speed  # Update the x position of the enemy
        self.y += direction_y * speed  # Update the y position of the enemy

        self.rect.topleft = (round(self.x), round(self.y))  # Update the position of the enemy's rectangle

        self.enemycollide(enemies)
    


enemies = [Enemy(), Enemy()]  # Erstelle eine Liste von Feinden

start_time = time.time()

run = True

global status
status = "running"

while run:
    # Limit frame rate
    pygame.time.Clock().tick(FPS)
    
    if status == "running":
        
        # Draw Background
        # screen.fill(WEISS)
        background_1_img = pygame.transform.scale(background_1_img, (screen_height, screen_height))
        screen.blit(background_1_img, (0, 0))
        # background_width, background_height = image.get_size()
        
        
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                # Store player position as a ratio of old screen size
                player_pos_ratio = [player_pos[0] / screen_width, player_pos[1] / screen_height]

                # Get new screen size
                (screen_width, screen_height) = event.size

                # Keep 16:9 aspect ratio
                # Calculate the aspect ratio dimensions
                aspect_width = min(screen_width, screen_height * (16/9))
                aspect_height = min(screen_height, screen_width * (9/16))

                # Set the screen size
                screen = pygame.display.set_mode((aspect_width, aspect_height), pygame.RESIZABLE)

                # Update player and enemy size
                player_size = (int(round((3/108) * screen_height)), int(round((3/108) * screen_height)))  # Größe des Spielers
                enemy_size = (int(round((3/108) * screen_height)), int(round((3/108) * screen_height)))  # Größe des Feindes

                # Scale player and enemy images
                player_still_img = pygame.transform.scale(player_still_img, player_size)
                enemy_goblin_img = pygame.transform.scale(enemy_goblin_img, enemy_size)
                
                # Scale background image
                background_1_img = pygame.transform.scale(background_1_img, (aspect_width, aspect_height))

                # Update player position based on new screen size
                player_pos[0] = min(player_pos_ratio[0] * screen_width, screen_width - player_size[0])
                player_pos[1] = min(player_pos_ratio[1] * screen_height, screen_height - player_size[1])
                    
                # Update enemy position and speed
                for enemy in enemies:
                    enemy.x = enemy.x * (screen_width/1280)
                    enemy.y = enemy.y * (screen_height/720)
                    enemy.rect.topleft = (round(enemy.x), round(enemy.y))
                    enemy_speed = 1 * ((screen_width/screen_height))
            
            # Quit Game
            if event.type == pygame.QUIT:
                run = False
                
            elif event.type == pygame.KEYDOWN:  # Ein Tastendruck-Ereignis
                if event.key == pygame.K_i:  # Die Taste "i" wurde gedrückt
                    if enemies:  # Überprüft, ob die Liste nicht leer ist
                        enemies.pop(0)  # Entfernt das erste Element aus der Liste

                elif event.key == pygame.K_o:  # Die Taste "o" wurde gedrückt
                    enemies.append(Enemy())  # Fügt einen neuen Feind zur Liste hinzu
                    enemies.append(Enemy())  # Fügt einen weiteren neuen Feind zur Liste hinzu

        # Enemy Object
        for enemy in enemies:
            enemy.update(player_pos, enemy_speed, enemies) # Update the enemy position

            # Calculate the angle between the enemy and the player
            enemy_pos_vector = pygame.math.Vector2((round(enemy.x), round(enemy.y)))
            player_pos_vector = pygame.math.Vector2(player_pos)
            direction = player_pos_vector - enemy_pos_vector
            angle = math.degrees(math.atan2(-direction.y, direction.x))

            # Rotate the enemy image to this angle
            enemy_goblin_img_rotated = pygame.transform.rotate(enemy_goblin_img, angle)

            # Draw Enemy Model
            screen.blit(enemy_goblin_img_rotated, (round(enemy.x), round(enemy.y)))
            
            if time.time()-start_time > 5:
                #Prüfe, ob sich die rechtecke Spieler und Gegner überlappen
                if player.colliderect(enemy.rect): 
                    print("Collision detected!")
                    # run = False  # Ende
        
        mouse_pos = pygame.mouse.get_pos() # Get Mouse Position
        
        # Set the cursor image
        pygame.mouse.set_visible(False)  # Hide the default cursor
        
        # Draw the cursor image at the mouse position
        screen.blit(cursor, pygame.mouse.get_pos())

        # Calculate the angle between the player and the mouse
        player_pos_vector = pygame.math.Vector2(player_pos)
        mouse_pos_vector = pygame.math.Vector2(mouse_pos)
        direction = mouse_pos_vector - player_pos_vector
        angle = math.degrees(math.atan2(-direction.y, direction.x))

        # Rotate the player image to this angle
        player_still_img_rotated = pygame.transform.rotate(player_still_img, angle)
        
        
        # --- Player ---
        # Erstelle das Spieler-Rechteck für die Darstellung und runde die Position auf die nächste Ganzzahl
        player_size = (int(round((5/100) * screen_height)), int(round((5/100) * screen_height)))  # Größe des Spielers
        player = pygame.Rect((round(player_pos[0]), round(player_pos[1])), player_size) # Create Player Rectangle
        # pygame.draw.rect(screen, blue, player) # Hitbox Player
        debug("Player and Enemy position when resizing",0,0) #DEBUG --------------------------------------------------------------------------------
        player_still_img_rotated = pygame.transform.scale(player_still_img_rotated, player_size) # Scale the player image
        screen.blit(player_still_img_rotated, (round(player_pos[0]), round(player_pos[1]))) # Draw Player Model

        key = pygame.key.get_pressed()
        if key[pygame.K_a] == True: 
            if player_pos[0] - move_speed < 0:
                player_pos[0] = 0
            else:
                player_pos[0] -= move_speed  # Move left
        if key[pygame.K_d] == True:
            if player_pos[0] + move_speed > screen_height - player_size[0]:
                player_pos[0] = screen_height - player_size[0]
            else:
                player_pos[0] += move_speed  # Move right
        if key[pygame.K_w] == True:
            if player_pos[1] - move_speed < 0:
                player_pos[1] = 0
            else:
                player_pos[1] -= move_speed  # Move up
        if key[pygame.K_s] == True:
            if player_pos[1] + move_speed > screen_height - player_size[1]:
                player_pos[1] = screen_height - player_size[1]
            else:
                player_pos[1] += move_speed  # Move down
        
        # Sidebar Information Screen
        wooden_background = pygame.transform.scale(wooden_background, (int(round(screen_width - screen_height)), screen_height))
        screen.blit(wooden_background, (int(round(screen_height)), 0, int(round(screen_width - screen_height)), screen_height))
        scroll_img = pygame.transform.scale(scroll_img, (int(round(screen_width - screen_height)), screen_height))
        screen.blit(scroll_img, (int(round(screen_height)), 0, int(round(screen_width - screen_height)), screen_height))
        # pygame.draw.rect(screen, SCHWARZ, (int(round(screen_height)), 0, int(round(screen_width - screen_height)), screen_height))

    pygame.display.update() #refresh screen
pygame.quit()

print("Game Closed")

