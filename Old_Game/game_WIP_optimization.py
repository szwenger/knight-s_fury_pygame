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

# Window Settings
pygame.display.set_caption("KNIGHT(ingale)") # Set the window title
pygame.display.set_icon(game_icon) # Set the window icon

screen = pygame.display.set_mode((screen_width, screen_height),pygame.RESIZABLE) # Set the screen size

# Enemy Class
class Enemy:
    def __init__(self):
        # Initialisiere die x- und y-Koordinaten des Feindes zufällig
        speed = 1 * ((screen_width/screen_height))  # Speed of the enemies
        
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

class Player:
    def __init__(self, player_still_img_rotated, screen_height, screen_width):
        self.player_size = (int(round((5/100) * screen_height)), int(round((5/100) * screen_height)))  # Größe des Spielers
        self.x = screen_height/2
        self.y = screen_height/2
        self.rect = pygame.Rect((round(self.x), round(self.y)), self.player_size) # Create Player Rectangle
        self.speed = 5
        self.image = pygame.transform.scale(player_still_img_rotated, self.player_size) # Scale the player image

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a] and self.x - self.speed > 0:  # left
            self.x -= self.speed
        if key[pygame.K_d] and self.x + self.speed < screen_width:  # right
            self.x += self.speed
        if key[pygame.K_w] and self.y - self.speed > 0:  # up
            self.y -= self.speed
        if key[pygame.K_s] and self.y + self.speed < screen_height:  # down
            self.y += self.speed
        self.rect.topleft = (self.x, self.y)  # Update the position of the rectangle

    def draw(self, screen):
        screen.blit(self.image, (round(self.x), round(self.y))) # Draw Player Model

    def collide(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                return True
        return False

    def update(self, screen, enemies):
        self.move()
        self.draw(screen)
        if self.collide(enemies):
            print("Collision detected!")
            # run = False  # End Game
    
# --- Main Variables ---

global status

status = "start_screen"  # Set the initial status of the game

# --- Functions ---

def resize_images():
    global player_still_img, enemy_goblin_img, background_1_img, wooden_background, scroll_img
    player_size = (int(round((3/108) * screen_height)), int(round((3/108) * screen_height)))  # Größe des Spielers
    enemy_size = (int(round((3/108) * screen_height)), int(round((3/108) * screen_height)))  # Größe des Feindes
    player_still_img = pygame.transform.scale(player_still_img, player_size)
    enemy_goblin_img = pygame.transform.scale(enemy_goblin_img, enemy_size)
    background_1_img = pygame.transform.scale(background_1_img, (screen_height, screen_height))
    wooden_background = pygame.transform.scale(wooden_background, (int(round(screen_width - screen_height)), screen_height))
    scroll_img = pygame.transform.scale(scroll_img, (int(round(screen_width - screen_height)), screen_height))

    # Sidebar Information Screen
def side_menu():
    global wooden_background, scroll_img
    wooden_background = pygame.transform.scale(wooden_background, (int(round(screen_width - screen_height)), screen_height))
    screen.blit(wooden_background, (int(round(screen_height)), 0, int(round(screen_width - screen_height)), screen_height))
    scroll_img = pygame.transform.scale(scroll_img, (int(round(screen_width - screen_height)), screen_height))
    screen.blit(scroll_img, (int(round(screen_height)), 0, int(round(screen_width - screen_height)), screen_height))
    # pygame.draw.rect(screen, SCHWARZ, (int(round(screen_height)), 0, int(round(screen_width - screen_height)), screen_height))


# Call the function to resize images when the game starts
resize_images()

enemies = [Enemy(), Enemy()]  # Erstelle eine Liste von Feinden

start_time = time.time()
run = True

while run:
    # Limit frame rate
    pygame.time.Clock().tick(FPS)
    
    # Draw Background
    screen.blit(background_1_img, (0, 0))
    
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

            # Update player position based on new screen size
            player_pos[0] = min(player_pos_ratio[0] * screen_width, screen_width - player_size[0])
            player_pos[1] = min(player_pos_ratio[1] * screen_height, screen_height - player_size[1])
                
            # Update enemy position and speed
            for enemy in enemies:
                enemy.x = enemy.x * (screen_width/1280)
                enemy.y = enemy.y * (screen_height/720)
                enemy.rect.topleft = (round(enemy.x), round(enemy.y))
                enemy_speed = 1 * ((screen_width/screen_height))

            # Call the function to resize images
            resize_images()
            
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
    
    player = Player(player_still_img_rotated, screen_height, screen_width)  # Create the player object
    player.update(screen, enemies)  # Update the player position
    
    # Draw the side menu
    side_menu()
    
    pygame.display.flip() #refresh screen
pygame.quit()

print("Game Closed")
