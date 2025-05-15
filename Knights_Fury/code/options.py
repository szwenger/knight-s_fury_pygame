import pygame, random, math
from constants import *

# ---------- Options Class ----------

class Options:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.inital_screen_width = screen_width
        self.initial_screen_height = screen_height

        # Absoluter Font-Pfad
        base_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_dir, "../_resources/public-pixel-font/PublicPixel-z84yD.ttf")

        # Sicherstellen, dass die Datei existiert
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")

        self.font = pygame.font.Font(font_path, screen_height//33)
        self.music_button = pygame.Rect(screen_width/3, screen_height/11, screen_width * (1/3), screen_height/11)
        self.sound_button = pygame.Rect(screen_width/3, screen_height * (3/11), screen_width * (1/3), screen_height/11)
        self.volume_slider = pygame.Rect(screen_width/3, screen_height * (5/11), screen_width * (1/3), screen_height/11)
        self.difficulty_slider = pygame.Rect(screen_width/3, screen_height * (7/11), screen_width * (1/3), screen_height/11)
        self.back_button = pygame.Rect(screen_width/3, screen_height * (9/11), screen_width * (1/3), screen_height/11)
        self.button_texture = pygame.image.load(get_path("_images", "Menu_Button.png"))
        self.button_texture = pygame.transform.scale(self.button_texture, (int(screen_width * (1/3)), int(screen_height/11)))
        self.music_button_text = "Music: On"
        self.sound_button_text = "Sound: On"
        
    def update_for_resize(self, new_screen_width, new_screen_height, snowflakes: list):
        width_ratio = new_screen_width / self.inital_screen_width
        height_ratio = new_screen_height / self.initial_screen_height

        for flake in snowflakes:
            flake['x'] = flake['x'] * width_ratio
            flake['y'] = flake['y'] * height_ratio

        self.screen_width = new_screen_width
        self.screen_height = new_screen_height
        self.music_button = pygame.Rect(new_screen_width/3, new_screen_height/11, new_screen_width * (1/3), new_screen_height/11)
        self.sound_button = pygame.Rect(new_screen_width/3, new_screen_height * (3/11), new_screen_width * (1/3), new_screen_height/11)
        self.volume_slider = pygame.Rect(new_screen_width/3, new_screen_height * (5/11), new_screen_width * (1/3), new_screen_height/11)
        self.difficulty_slider = pygame.Rect(new_screen_width/3, new_screen_height * (7/11), new_screen_width * (1/3), new_screen_height/11)
        self.back_button = pygame.Rect(new_screen_width/3, new_screen_height * (9/11), new_screen_width * (1/3), new_screen_height/11)
        self.font = pygame.font.Font(get_path("_resources", "public-pixel-font", "PublicPixel-z84yD.ttf"), new_screen_height // 33)
        self.button_texture = pygame.transform.scale(self.button_texture, (int(new_screen_width * (1/3)), int(new_screen_height/11)))       
        
    def background_snowfall(self, screen, snowflakes: list):
        screen.fill((0, 0, 0))  # Black background

        for flake in snowflakes:
            pygame.draw.circle(screen, (255, 255, 255), (flake['x'], flake['y']), flake['size'])  # Draw snowflake

            flake['y'] += flake['speed']  # Move snowflake down
            flake['x'] += random.choice([-1, 0, 1])  # Slight horizontal drift

            # If snowflake has fallen off the screen, reset it to the top
            if flake['y'] > self.screen_height:
                flake['y'] = 0
                flake['x'] = random.randint(0, self.screen_width)
                flake['speed'] = random.randint(1, 3)  # Random speed
                flake['size'] = random.randint(1, 3)  # Random size
        
        
    def draw(self, screen, snowflakes: list):
        self.background_snowfall(screen, snowflakes)

        buttons = [
            (self.music_button_text, self.music_button),
            (self.sound_button_text, self.sound_button),
            ('Volume: WIP', self.volume_slider),
            ('Difficulty: WIP', self.difficulty_slider),
            ('Back', self.back_button)
        ]

        for text, button in buttons:
            pygame.draw.rect(screen, (255, 255, 255), button)
            screen.blit(self.button_texture, (button.x, button.y))

            label = self.font.render(text, True, (0, 0, 0))
            label_rect = label.get_rect()  # Get the rectangle that encloses the text
            label_rect.center = button.center  # Set the center of the rectangle to the center of the button
            screen.blit(label, label_rect)
        
        