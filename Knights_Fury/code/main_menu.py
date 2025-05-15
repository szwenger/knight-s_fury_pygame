import pygame, random, math
from constants import *

# ---------- Main Menu Class ----------

class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.width = int(round(screen_width))
        self.height = int(round(screen_height))
        self.size = (self.width, self.height)

        # Absoluter Font-Pfad
        base_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_dir, "../_resources/public-pixel-font/PublicPixel-z84yD.ttf")

        # Sicherstellen, dass die Datei existiert
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")

        self.font_size = int(round((1/15) * self.height))
        self.font = pygame.font.Font(font_path, self.font_size) # Load the font
        self.rect = pygame.Rect((0, 0), self.size)
        self.background = menu_background
        self.background = pygame.transform.scale(self.background, self.size)
        self.background_grasslayer = menu_background_grasslayer
        self.background_grasslayer = pygame.transform.scale(self.background_grasslayer, (self.width * 1.1, self.width * 1.1))
        self.background_grasslayer_x = -50
        self.background_grasslayer_y = 0
        self.time = 0
        self.amplitude = 1.5
        self.frequency = 0.1
        self.button_background = menu_button
        self.button_background = pygame.transform.scale(self.button_background, (int(round((1/3)*self.width)), int(round((1/7)*self.height))))
        self.start_rect = pygame.Rect((int(round((1/3) * self.width)), int(round((1/7) * self.height))), (int(round((1/3)*self.width)), int(round((1/7)*self.height))))
        self.options_rect = pygame.Rect((int(round((1/3) * self.width)), int(round((3/7) * self.height))), (int(round((1/3)*self.width)), int(round((1/7)*self.height))))
        self.quit_rect = pygame.Rect((int(round((1/3) * self.width)), int(round((5/7) * self.height))), (int(round((1/3)*self.width)), int(round((1/7)*self.height))))
        
    def start_button(self, screen):
        start_text = "Start"
        text_surface = self.font.render(start_text, True, (0, 0, 0))
        text_dimensions = text_surface.get_size()
        screen.blit(self.button_background, self.start_rect.topleft)
        screen.blit(text_surface, (int(round((1/3) * self.width)) + int(round((1/6)*self.width)) - int(round((1/2) * text_dimensions[0])), int(round((1/7) * self.height)) + int(round((1/14)*self.height)) - int(round((1/2) * text_dimensions[1]))))
        
    def options_button(self, screen):
        screen.blit(self.button_background, self.options_rect.topleft)
        options_text = "Options"
        text_surface = self.font.render(options_text, True, (0, 0, 0))
        text_dimensions = text_surface.get_size()
        screen.blit(text_surface, (int(round((1/3) * self.width)) + int(round((1/6)*self.width)) - int(round((1/2) * text_dimensions[0])), int(round((3/7) * self.height)) + int(round((1/14)*self.height)) - int(round((1/2) * text_dimensions[1]))))
        
    def quit_button(self, screen):
        screen.blit(self.button_background, self.quit_rect.topleft)
        quit_text = "Quit"
        text_surface = self.font.render(quit_text, True, (0, 0, 0))
        text_dimensions = text_surface.get_size()
        screen.blit(text_surface, (int(round((1/3) * self.width)) + int(round((1/6)*self.width)) - int(round((1/2) * text_dimensions[0])), int(round((5/7) * self.height)) + int(round((1/14)*self.height)) - int(round((1/2) * text_dimensions[1]))))        
        
    def draw(self, screen, current_time, start_time):
        screen.blit(self.background, (0, 0))
        self.time += 1
        self.background_grasslayer_x += self.amplitude * math.sin(self.frequency * self.time)
        screen.blit(self.background_grasslayer, (self.background_grasslayer_x, self.background_grasslayer_y))
        self.start_button(screen)
        self.options_button(screen)
        self.quit_button(screen)
        
    def update_for_resize(self, new_screen_width, new_screen_height):
        self.height = new_screen_height
        self.width = new_screen_width
        self.size = (self.width, self.height)
        self.font_size = int(round((1/15) * self.height))
        self.font = pygame.font.Font(get_path("_resources", "public-pixel-font", "PublicPixel-z84yD.ttf"), self.font_size)
        self.rect.size = self.size
        self.rect = pygame.Rect((0, 0), self.size)
        self.button_background = menu_button
        self.button_background = pygame.transform.scale(self.button_background, (int(round((1/3)*self.width)), int(round((1/7)*self.height))))
        self.start_rect = pygame.Rect(int(round((1/3) * self.width)), int(round((1/7) * self.height)), int(round((1/3)*self.width)), int(round((1/7)*self.height)))
        self.options_rect = pygame.Rect(int(round((1/3) * self.width)), int(round((3/7) * self.height)), int(round((1/3)*self.width)), int(round((1/7)*self.height)))
        self.quit_rect = pygame.Rect(int(round((1/3) * self.width)), int(round((5/7) * self.height)), int(round((1/3)*self.width)), int(round((1/7)*self.height)))
        self.background = menu_background
        self.background = pygame.transform.scale(self.background, self.size)
        self.background_grasslayer = menu_background_grasslayer
        self.background_grasslayer = pygame.transform.scale(self.background_grasslayer, (self.width, self.width))