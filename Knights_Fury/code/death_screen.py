import pygame, random, math
from constants import *
from player import Player
from field import Field

# ---------- Death Screen Class ----------

class Death_Screen:
    def __init__ (self, screen, player: Player, field: Field):
        self.screen = screen
        self.player = player
        self.field = field

        # Absoluter Font-Pfad
        base_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_dir, "../_resources/public-pixel-font/PublicPixel-z84yD.ttf")

        # Sicherstellen, dass die Datei existiert
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")

        self.big_font = pygame.font.Font(font_path, (int(field.sidelength/10)))
        self.normal_font = pygame.font.Font(font_path, (int(field.sidelength/20)))
        self.small_font = pygame.font.Font(font_path, (int(field.sidelength/30)))
        self.button_image = pygame.image.load(get_path("_images", "Menu_Button.png"))
        self.restart_button = pygame.Rect(field.sidelength/4, field.sidelength/7, self.field.sidelength/2, self.field.sidelength/7)
        self.main_menu_button = pygame.Rect(field.sidelength/4, field.sidelength * (3/7), self.field.sidelength/2, self.field.sidelength/7)
        self.quit_button = pygame.Rect(field.sidelength/4, field.sidelength * (5/7), self.field.sidelength/2, self.field.sidelength/7)
        self.button_image = pygame.transform.scale(self.button_image, self.restart_button.size)
        self.background = None
        
    def draw_text(self, text, font, color, x, y, outline_color=(0, 0, 0)):
        text_surface = font.render(text, True, color)
        outline_surface = font.render(text, True, outline_color)

        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)

        # Draw the outline
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            outline_rect = text_rect.copy()
            outline_rect.move_ip(dx, dy)
            self.screen.blit(outline_surface, outline_rect)

        # Draw the text
        self.screen.blit(text_surface, text_rect)
    
    def draw(self, enemies: list):
        self.player.health = 1
        self.player.x = self.field.sidelength/2
        self.player.y = self.field.sidelength/2
        enemies.clear()
        # self.field.draw(self.screen)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.button_image, self.restart_button)
        self.screen.blit(self.button_image, self.main_menu_button)
        self.screen.blit(self.button_image, self.quit_button)
        self.draw_text('You Died', self.big_font, (255, 0, 0), self.field.sidelength/2, self.field.sidelength/14)
        self.draw_text('Restart', self.normal_font, (255, 255, 255), self.field.sidelength/2, self.field.sidelength/7 + self.field.sidelength/14)
        self.draw_text('Main Menu', self.normal_font, (255, 255, 255), self.field.sidelength/2, self.field.sidelength * (3/7) + self.field.sidelength/14)
        self.draw_text('Quit', self.normal_font, (255, 255, 255), self.field.sidelength/2, self.field.sidelength * (5/7) + self.field.sidelength/14)
        
    def update_for_resize(self, new_fieldlength):
        self.big_font = pygame.font.Font(get_path("_resources", "public-pixel-font", "PublicPixel-z84yD.ttf"), int(new_fieldlength / 10))
        self.normal_font = pygame.font.Font(get_path("_resources", "public-pixel-font", "PublicPixel-z84yD.ttf"), int(new_fieldlength / 20))
        self.small_font = pygame.font.Font(get_path("_resources", "public-pixel-font", "PublicPixel-z84yD.ttf"), int(new_fieldlength / 30))
        self.restart_button = pygame.Rect(new_fieldlength / 4, new_fieldlength / 7, new_fieldlength / 2, new_fieldlength / 7)
        self.main_menu_button = pygame.Rect(new_fieldlength * (3 / 7), new_fieldlength / 4, new_fieldlength / 2, new_fieldlength / 7)
        self.quit_button = pygame.Rect(new_fieldlength * (5 / 7), new_fieldlength / 4, new_fieldlength / 2, new_fieldlength / 7)
        self.button_image = pygame.transform.scale(self.button_image, self.restart_button.size)