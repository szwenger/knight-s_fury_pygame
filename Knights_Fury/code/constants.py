import os
import pygame
import spritesheet

pygame.font.init()
pygame.mixer.init()

# ---------- Constants ----------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of this script

# Helper function to construct paths
def get_path(*args):
    return os.path.join(BASE_DIR, "..", *args)

# --- Debugging ---
print(f"Script running from: {BASE_DIR}")

# --- Verify Image Paths Before Loading ---
IMAGE_PATH = get_path("_images", "Knights_Fury.png")
print(f"Trying to load image from: {IMAGE_PATH}")

if not os.path.exists(IMAGE_PATH):
    raise FileNotFoundError(f"File not found: {IMAGE_PATH}")

# --- Colors ---
SCHWARZ = (0, 0, 0)
BLAU    = (17, 69, 126)
ROT     = (255, 0, 0)
ROT2    = (215, 20, 26)
ROT3    = (238, 0, 0)
WEISS   = (255, 255, 255)
GRUEN   = (46, 139, 87)
GELB    = (255, 215, 0)
GOLD    = (255, 206, 0)
SKYBLUE = (108, 172, 228)
BLUE    = (0, 20, 137)
GBRED   = (200, 16, 46)
GBBLUE  = (0, 36, 125)

# --- Images ---
icon = pygame.image.load(get_path("_images", "Knights_Fury.png"))
game_icon = pygame.transform.scale(icon, (32, 32))

enemy_goblin_img = pygame.image.load(get_path("_images", "_enemies", "enemy_goblin_default.png"))
orc_img = pygame.image.load(get_path("_images", "_enemies", "enemy_orc.png"))
archer_img = pygame.image.load(get_path("_images", "_enemies", "enemy_goblin__archer_default.png"))
ogre_img = pygame.image.load(get_path("_images", "_enemies", "ogre_default.png"))

background_1_img = pygame.image.load(get_path("_images", "Background_default2_1200x1200.png"))
menu_background = pygame.image.load(get_path("_images", "Background_menu_1200x1200.png"))
menu_background_grasslayer = pygame.image.load(get_path("_images", "Background_menu_grasslayer_1200x1200_v3.png"))

scroll_img = pygame.image.load(get_path("_images", "side_menu_kindpng_5697892.png"))
wooden_background = pygame.image.load(get_path("_images", "wooden_texture.png"))

cursor_img = pygame.image.load(get_path("_images", "Sword_Cursor.png"))
arrow_img = pygame.image.load(get_path("_images", "arrow_img.png"))
menu_button = pygame.image.load(get_path("_images", "Menu_Button.png"))

# --- Sprites ---
knight_sprite = pygame.image.load(get_path("_images", "_player", "Knight_sprite_sheet2.png"))
knight_sprite_sheet = spritesheet.SpriteSheet(knight_sprite)

# Knight Still Sprite
knight_still_sprite = knight_sprite_sheet.get_image(0, 30, 30, 2)

# Knight Moving Sprites
knight_sprites = [knight_sprite_sheet.get_image(i, 30, 30, 2) for i in range(1, 3)]
animation_cooldown = 300 # Set the cooldown for the animation
frame = 0 # Set the frame to 0

# Sword Sprite
sword_sprite_raw = pygame.image.load(get_path("_images", "_player", "AnimatedSwordv3.png"))
sword_spritesheet = spritesheet.SpriteSheet(sword_sprite_raw)
sword_sprites = [sword_spritesheet.get_image(i, 90, 90, 1) for i in range(0, 9)]

# --- Sounds ---
player_sword_miss = [
    pygame.mixer.Sound(get_path("_sounds", "Minifantasy_Dungeon_SFX", "07_human_atk_sword_1.wav")),
    pygame.mixer.Sound(get_path("_sounds", "Minifantasy_Dungeon_SFX", "07_human_atk_sword_2.wav")),
    pygame.mixer.Sound(get_path("_sounds", "Minifantasy_Dungeon_SFX", "07_human_atk_sword_3.wav")),
]

player_sword_hit = [
    pygame.mixer.Sound(get_path("_sounds", "Minifantasy_Dungeon_SFX", "26_sword_hit_1.wav")),
    pygame.mixer.Sound(get_path("_sounds", "Minifantasy_Dungeon_SFX", "26_sword_hit_2.wav")),
    pygame.mixer.Sound(get_path("_sounds", "Minifantasy_Dungeon_SFX", "26_sword_hit_3.wav")),
]

player_damage = [
    pygame.mixer.Sound(get_path("_sounds", "Minifantasy_Dungeon_SFX", "11_human_damage_1.wav")),
    pygame.mixer.Sound(get_path("_sounds", "Minifantasy_Dungeon_SFX", "11_human_damage_2.wav")),
    pygame.mixer.Sound(get_path("_sounds", "Minifantasy_Dungeon_SFX", "11_human_damage_3.wav")),
]

# --- Fonts ---
font = pygame.font.Font(get_path("_resources", "public-pixel-font", "PublicPixel-z84yD.ttf"), 30)

# --- Variables ---
FPS = 60
