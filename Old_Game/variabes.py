import pygame
#variables

# --- colors ---
SCHWARZ = (0,0,0)
BLAU    = (17,69,126)
ROT     = (255,0,0)
ROT2    = (215,20,26)
ROT3    = (238,0,0)
WEISS   = (255,255,255)
GRUEN   = (46,139,87)
GELB    = (255,215,0)
GOLD    = (255,206,0)
SKYBLUE = (108, 172, 228)
BLUE    = (0, 20, 137)
GBRED   = (200, 16, 46)
GBBLUE  = (0, 36, 125)


# --- Screen ---
screen_width = 1280
screen_height = 720

# --- Images ---
icon = pygame.image.load('_images\_player\Knight_icon.png') # Load the game icon
game_icon = pygame.transform.scale(icon, (32, 32)) # Scale the game icon

player_still_img = pygame.image.load('_images/_player/Knight_empty.png') # Load the player image
# player_still_img = pygame.transform.scale(player_still_img, (int(round((3/20) * screen_height)), int(round((3/20) * screen_height)))) # Scale the player image
enemy_goblin_img = pygame.image.load('_images/enemy_goblin_default.png') # Load the enemy image
# enemy_goblin_img = pygame.transform.scale(enemy_goblin_img, (int(round((3/20) * screen_height)), int(round((3/20) * screen_height)))) # Scale the enemy image

# background_1_img = pygame.image.load('_images/Background_default.png') # Old Background Image
background_1_img = pygame.image.load('_images\Background_default_1200x1200.png') # Load the background image
scroll_img = pygame.image.load('_images\side_menu_kindpng_5697892.png') # Load the scroll image
cursor = pygame.image.load('_images\Sword_Cursor.png') # Load the cursor image
wooden_background = pygame.image.load('_images\wooden_texture.png') # Load the wooden background image

# --- Create Player ---
player_pos = [screen_height/2, screen_height/2]  # Position des Spielers als Gleitkommazahl
move_speed = 3 * ((screen_width/screen_height))
#player_size = (int(round((3/108) * screen_height)), int(round((3/108) * screen_height)))  # Größe des Spielers

# --- Enemy ---
enemy_speed = 1 * ((screen_width/screen_height))  # Geschwindigkeit der Feinde

FPS = 60