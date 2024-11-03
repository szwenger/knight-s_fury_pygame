import pygame, random, math, time
from constants import *

# ---------- Start Screen Class ----------

class Start_Screen:
    def __init__ (self, screen, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.inital_screen_width = screen_width
        self.initial_screen_height = screen_height
        self.size = (self.width, self.height)
        self.rect = pygame.Rect((0, 0), self.size)
        self.font_size = int(round((1/6) * self.height))        
        self.font = pygame.font.Font('Knights_Fury/_resources/public-pixel-font/PublicPixel-z84yD.ttf', self.font_size)
        self.top_text = "KNIGHT'S"
        self.bottom_text = "FURY"
        self.logo = icon
        self.logo = pygame.transform.scale(self.logo, (int(round((1/2)*self.height)), int(round((1/2)*self.height))))
    
    def background_snowfall(self, screen, snowflakes: list):
        screen.fill((0, 0, 0))  # Black background

        for flake in snowflakes:

            pygame.draw.circle(screen, (255, 255, 255), (flake['x'], flake['y']), flake['size'])  # Draw snowflake
            flake['y'] += flake['speed']  # Move snowflake down
            flake['x'] += random.choice([-1, 0, 1])  # Slight horizontal drift
            # If snowflake has fallen off the screen, reset it to the top

            if flake['y'] > self.height:
                flake['y'] = 0
                flake['x'] = random.randint(0, self.width)
                flake['speed'] = random.randint(1, 3)  # Random speed
                flake['size'] = random.randint(1, 3)  # Random size
                
    def draw_text(self, screen, text, font, color, x, y, outline_color=(0, 0, 0)):
        text_surface = font.render(text, True, color)
        outline_surface = font.render(text, True, outline_color)

        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)

        # Draw the outline
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            outline_rect = text_rect.copy()
            outline_rect.move_ip(dx, dy)
            screen.blit(outline_surface, outline_rect)

        # Draw the text
        screen.blit(text_surface, text_rect)
                
    def update_for_resize(self, new_screen_width, new_screen_height, snowflakes: list):
        width_ratio = new_screen_width / self.inital_screen_width
        height_ratio = new_screen_height / self.initial_screen_height

        for flake in snowflakes:
            flake['x'] = flake['x'] * width_ratio
            flake['y'] = flake['y'] * height_ratio

        self.width = new_screen_width
        self.height = new_screen_height
        self.size = (self.width, self.height)
        self.rect.size = self.size
        self.rect = pygame.Rect((0, 0), self.size)
        self.logo = pygame.transform.scale(self.logo, (int(round((1/2)*self.height)), int(round((1/2)*self.height))))
        self.font_size = int(round((1/6) * self.height))
        self.font = pygame.font.Font('Knights_Fury/_resources/public-pixel-font/PublicPixel-z84yD.ttf', self.font_size)
        
                                          
    def draw(self, screen, snowflakes: list, started_game: float, current_time: float):
        self.background_snowfall(screen, snowflakes)
        
        if current_time - started_game > 1200:
            logo_x = self.width/2 - self.logo.get_size()[0] * (1/2)
            logo_y = self.height/2 - self.logo.get_size()[1] * (1/2)
            if ((current_time - started_game) // 10) < 255:
                self.logo.set_alpha(int(round((current_time - started_game) // 10)))
            screen.blit(self.logo, (logo_x, logo_y))

        if current_time - started_game > 3000:
            alpha = min(255, int(round((current_time - started_game - 3000) // 10)))
            top_text_surface = self.font.render(self.top_text, True, (255, 0, 0))
            bottom_text_surface = self.font.render(self.bottom_text, True, (255, 0, 0))
            top_text_surface.set_alpha(alpha)
            bottom_text_surface.set_alpha(alpha)
            screen.blit(top_text_surface, (self.width/2 - top_text_surface.get_width() / 2, self.height/2 - self.font_size/2))
            screen.blit(bottom_text_surface, (self.width/2 - bottom_text_surface.get_width() / 2, self.height/2 + self.font_size/2))
            
        if current_time - started_game > 9000:
            fade_out_background = pygame.Surface((self.width, self.height))
            fade_out_background.fill((0, 0, 0))
            fade_out_background.set_alpha(int(round((current_time - started_game - 9000) // 4))
            )
            screen.blit(fade_out_background, (0, 0)) 