import pygame
import random
import os
from constants import *

# ---------- Start Screen Class ----------

class Start_Screen:
    def __init__ (self, screen, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.initial_screen_width = screen_width
        self.initial_screen_height = screen_height
        self.size = (self.width, self.height)
        self.rect = pygame.Rect((0, 0), self.size)
        self.font_size = int(round((1/6) * self.height))

        # Absoluter Font-Pfad
        base_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_dir, "../_resources/public-pixel-font/PublicPixel-z84yD.ttf")

        # Sicherstellen, dass die Datei existiert
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")

        self.font = pygame.font.Font(font_path, self.font_size)
        self.top_text = "KNIGHT'S"
        self.bottom_text = "FURY"
        self.logo = icon  # Falls icon in constants.py definiert ist
        self.logo = pygame.transform.scale(self.logo, (int(round((1/2) * self.height)), int(round((1/2) * self.height))))

    def background_snowfall(self, screen, snowflakes: list):
        screen.fill((0, 0, 0))  # Schwarzer Hintergrund

        for flake in snowflakes:
            pygame.draw.circle(screen, (255, 255, 255), (flake['x'], flake['y']), flake['size'])  # Schneeflocke zeichnen
            flake['y'] += flake['speed']  # Nach unten bewegen
            flake['x'] += random.choice([-1, 0, 1])  # Leicht horizontale Drift

            # Falls Schneeflocke unten aus dem Bildschirm fällt, neu oben platzieren
            if flake['y'] > self.height:
                flake['y'] = 0
                flake['x'] = random.randint(0, self.width)
                flake['speed'] = random.randint(1, 3)
                flake['size'] = random.randint(1, 3)

    def draw_text(self, screen, text, font, color, x, y, outline_color=(0, 0, 0)):
        text_surface = font.render(text, True, color)
        outline_surface = font.render(text, True, outline_color)
        text_rect = text_surface.get_rect(center=(x, y))

        # Textumrandung zeichnen
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            screen.blit(outline_surface, text_rect.move(dx, dy))

        # Haupttext zeichnen
        screen.blit(text_surface, text_rect)

    def update_for_resize(self, new_screen_width, new_screen_height, snowflakes: list):
        width_ratio = new_screen_width / self.initial_screen_width
        height_ratio = new_screen_height / self.initial_screen_height

        for flake in snowflakes:
            flake['x'] *= width_ratio
            flake['y'] *= height_ratio

        self.width = new_screen_width
        self.height = new_screen_height
        self.size = (self.width, self.height)
        self.rect.size = self.size
        self.rect = pygame.Rect((0, 0), self.size)
        self.logo = pygame.transform.scale(self.logo, (int(round((1/2) * self.height)), int(round((1/2) * self.height))))
        self.font_size = int(round((1/6) * self.height))

        # Font mit neuer Größe laden
        base_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_dir, "../_resources/public-pixel-font/PublicPixel-z84yD.ttf")
        self.font = pygame.font.Font(font_path, self.font_size)

    def draw(self, screen, snowflakes: list, started_game: float, current_time: float):
        self.background_snowfall(screen, snowflakes)

        if current_time - started_game > 1200:
            logo_x = self.width / 2 - self.logo.get_width() / 2
            logo_y = self.height / 2 - self.logo.get_height() / 2
            alpha = min(255, int((current_time - started_game) // 10))
            self.logo.set_alpha(alpha)
            screen.blit(self.logo, (logo_x, logo_y))

        if current_time - started_game > 3000:
            alpha = min(255, int((current_time - started_game - 3000) // 10))
            top_text_surface = self.font.render(self.top_text, True, (255, 0, 0))
            bottom_text_surface = self.font.render(self.bottom_text, True, (255, 0, 0))
            top_text_surface.set_alpha(alpha)
            bottom_text_surface.set_alpha(alpha)
            screen.blit(top_text_surface, (self.width / 2 - top_text_surface.get_width() / 2, self.height / 2 - self.font_size / 2))
            screen.blit(bottom_text_surface, (self.width / 2 - bottom_text_surface.get_width() / 2, self.height / 2 + self.font_size / 2))

        if current_time - started_game > 9000:
            fade_out_background = pygame.Surface((self.width, self.height))
            fade_out_background.fill((0, 0, 0))
            fade_alpha = int((current_time - started_game - 9000) // 4)
            fade_out_background.set_alpha(min(255, fade_alpha))
            screen.blit(fade_out_background, (0, 0))
