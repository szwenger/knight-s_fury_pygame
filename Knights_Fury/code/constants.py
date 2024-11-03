import pygame
import spritesheet

pygame.font.init()
pygame.mixer.init()

# ---------- Constants ----------

# --- Colors ---
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

# --- Images ---
icon = pygame.image.load("Knights_Fury/_images/Knights_Fury.png") # Load the game icon
game_icon = pygame.transform.scale(icon, (32, 32)) # Scale the game icon

# player_still_img = pygame.image.load('Knights_Fury/_images/_player/Knight_empty.png') # Load the player image
enemy_goblin_img = pygame.image.load('Knights_Fury/_images/_enemies/enemy_goblin_default.png') # Load the enemy image
orc_img = pygame.image.load('Knights_Fury/_images/_enemies/enemy_orc.png') # Load the enemy image
archer_img = pygame.image.load('Knights_Fury/_images/_enemies/enemy_goblin__archer_default.png') # Load the enemy image
ogre_img = pygame.image.load('Knights_Fury/_images/_enemies/ogre_default.png') # Load the enemy image

background_1_img = pygame.image.load('Knights_Fury/_images/Background_default2_1200x1200.png') # Load the background image

menu_background = pygame.image.load('Knights_Fury/_images/Background_menu_1200x1200.png') # Load the menu background image
menu_background_grasslayer = pygame.image.load('Knights_Fury/_images/Background_menu_grasslayer_1200x1200_v3.png') # Load the menu background grass layer image

scroll_img = pygame.image.load('Knights_Fury/_images/side_menu_kindpng_5697892.png') # Load the scroll image
wooden_background = pygame.image.load('Knights_Fury/_images/wooden_texture.png') # Load the wooden background image

cursor_img = pygame.image.load('Knights_Fury/_images/Sword_Cursor.png') # Load the cursor image

arrow_img = pygame.image.load('Knights_Fury/_images/arrow_img.png') # Load the arrow image

menu_button = pygame.image.load('Knights_Fury/_images/Menu_Button.png') # Load the menu button image

# --- Sprites ---

# Knight Sprite
knight_sprite = pygame.image.load('Knights_Fury/_images/_player/Knight_sprite_sheet2.png') # Load the knight sprite/
knight_sprite_sheet = spritesheet.SpriteSheet(knight_sprite) # Create a spritesheet object

# Knight Still Sprite
knight_still_sprite = knight_sprite_sheet.get_image(0, 30, 30, 2) # Get the image for the knight still sprite

# Knight Moving Sprites
knight_sprites = [] # Create a list to store the knight sprites
for i in range(1, 3, 1): # Iterate through the animation steps
    knight_sprites.append(knight_sprite_sheet.get_image(i, 30, 30, 2)) # Get the image for the current animation step

animation_cooldown = 300 # Set the cooldown for the animation
frame = 0 # Set the frame to 0

# Sword Sprite
sword_sprite_raw = pygame.image.load('Knights_Fury/_images/_player/AnimatedSwordv3.png') # Load the sword sprite
sword_spritesheet = spritesheet.SpriteSheet(sword_sprite_raw) # Create a spritesheet object
sword_sprites = [] # Create a list to store the sword sprites

for i in range(0, 9, 1): # Iterate through the animation steps
    sword_sprites.append(sword_spritesheet.get_image(i, 90, 90, 1)) # Get the image for the current animation step

# --- Sounds ---

# main_menu_music = pygame.mixer.music.load('Knights_Fury/_sounds/Minifantasy_Dungeon_Music/Music/Goblins_Den_(Regular).wav') # Load the main menu music
# battle_music = pygame.mixer.music.load('Knights_Fury/_sounds/Minifantasy_Dungeon_Music/Music/Goblins_Dance_(Battle).wav') # Load the battle music

# Player Sounds

player_sword_miss = [
pygame.mixer.Sound('Knights_Fury/_sounds/Minifantasy_Dungeon_SFX/07_human_atk_sword_1.wav'), # Load the player sword miss sound
pygame.mixer.Sound('Knights_Fury/_sounds/Minifantasy_Dungeon_SFX/07_human_atk_sword_2.wav'), # Load the player sword miss sound
pygame.mixer.Sound('Knights_Fury/_sounds/Minifantasy_Dungeon_SFX/07_human_atk_sword_3.wav'), # Load the player sword miss sound
]

player_sword_hit = [
pygame.mixer.Sound('Knights_Fury/_sounds/Minifantasy_Dungeon_SFX/26_sword_hit_1.wav'), # Load the player sword hit sound
pygame.mixer.Sound('Knights_Fury/_sounds/Minifantasy_Dungeon_SFX/26_sword_hit_2.wav'), # Load the player sword hit sound
pygame.mixer.Sound('Knights_Fury/_sounds/Minifantasy_Dungeon_SFX/26_sword_hit_3.wav') # Load the player sword hit sound
]

player_damage = [
pygame.mixer.Sound('Knights_Fury/_sounds/Minifantasy_Dungeon_SFX/11_human_damage_1.wav'), # Load the player damage sound
pygame.mixer.Sound('Knights_Fury/_sounds/Minifantasy_Dungeon_SFX/11_human_damage_2.wav'), # Load the player damage sound
pygame.mixer.Sound('Knights_Fury/_sounds/Minifantasy_Dungeon_SFX/11_human_damage_3.wav'), # Load the player damage sound
]

# --- Fonts ---

font = pygame.font.Font('Knights_Fury/_resources/public-pixel-font/PublicPixel-z84yD.ttf', 30) # Load the font

# --- Variables ---

# --- Immutable Variables ---

FPS = 60