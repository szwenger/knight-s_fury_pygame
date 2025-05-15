import pygame, random, math
from constants import *

# Side Menu Class

class SideMenu:
    def __init__(self, screen_width, screen_height):
        self.position = (screen_height, 0)
        self.size = (screen_width - screen_height, screen_height)
        self.rect = pygame.Rect((screen_height, 0), self.size)

        # Absoluter Font-Pfad
        base_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_dir, "../_resources/public-pixel-font/PublicPixel-z84yD.ttf")

        # Sicherstellen, dass die Datei existiert
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")

        self.font_size = int(round((1/35) * self.size[1]))
        self.font = pygame.font.Font(font_path, self.font_size) # Load the fonthe font
        self.background = wooden_background
        self.background = pygame.transform.scale(self.background, self.size)
        self.texture = scroll_img
        self.texture = pygame.transform.scale(self.texture, self.size)
    
    def draw(self, screen):
        screen.blit(self.background, (self.rect.topleft))
        screen.blit(self.texture, (self.rect.topleft))
        
    def update_for_resize(self, new_screen_width, new_screen_height):
        self.position = (new_screen_height, 0)
        self.size = (new_screen_width - new_screen_height, new_screen_height)
        self.rect.size = self.size
        self.rect = pygame.Rect((new_screen_height, 0), self.size)
        self.font_size = int(round((1/35) * self.size[1]))
        self.font = pygame.font.Font(get_path("_resources", "public-pixel-font", "PublicPixel-z84yD.ttf"), self.font_size)
        self.background = pygame.transform.scale(wooden_background, self.size)
        self.background = pygame.transform.scale(self.background, self.size)        
        self.texture = pygame.transform.scale(scroll_img, self.size)
        self.texture = pygame.transform.scale(self.texture, self.size)
    
    def draw_info(self, screen, health: int, kills: int, time: float, arrow_count:int, wave:int, score, highscore):
        font = pygame.font.Font(get_path("_resources", "public-pixel-font", "PublicPixel-z84yD.ttf"), int(round((1/25) * screen.get_height())))
        health_text = "Health: " + str(health)
        kills_text = "Kills: " + str(kills)
        time_text = "Time: " + str(time)
        arrows_text = "Arrows: " +str(arrow_count)
        wave_text = "Wave: " +str(wave)
        score_text = "Score: " +str(score)
        highscore_text = "Top: " + str(highscore)

        health_surface = font.render(health_text, True, (0, 0, 0))
        kills_surface = font.render(kills_text, True, (0, 0, 0))
        time_surface = font.render(time_text, True, (0, 0, 0))
        arrow_surface = font.render(arrows_text, True, (0, 0, 0))
        wave_surface = font.render(wave_text, True, (0, 0, 0))
        score_surface = font.render(score_text, True, (0, 0, 0))
        highscore_surface = font.render(highscore_text, True, (0, 0, 0))


        screen.blit(wave_surface, (int(round(self.position[0] + (1/4) * self.size[0])), int(round((3/20) * self.size[1]))))
        screen.blit(time_surface, (int(round(self.position[0] + (1/4) * self.size[0])), int(round((5/20) * self.size[1]))))
        screen.blit(health_surface, (int(round(self.position[0] + (1/4) * self.size[0])), int(round((8/20) * self.size[1]))))
        screen.blit(kills_surface, (int(round(self.position[0] + (1/4) * self.size[0])), int(round((10/20) * self.size[1]))))
        screen.blit(arrow_surface, (int(round(self.position[0] + (1/4) * self.size[0])), int(round((12/20) * self.size[1]))))
        
        screen.blit(highscore_surface, (int(round(self.position[0] + (1/4) * self.size[0])), int(round((15/20) * self.size[1]))))
        screen.blit(score_surface, (int(round(self.position[0] + (1/4) * self.size[0])), int(round((16/20) * self.size[1]))))

