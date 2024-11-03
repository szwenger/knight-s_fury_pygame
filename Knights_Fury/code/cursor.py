import pygame, random, math
from constants import *

# ---------- Cursor Class ----------

class Cursor:
    def __init__(self):
        self.size = (32, 32)
        self.texture = cursor_img
        self.texture = pygame.transform.scale(self.texture, self.size)
        self.position = (0, 0)
        self.rect = pygame.Rect(self.position, self.size)
        
    def draw(self, screen):
        self.position = pygame.mouse.get_pos()
        self.rect.topleft = self.position
        screen.blit(self.texture, self.position)
        
    def update_for_resize(self, new_screen_height):
        self.size = (int(round((2/45) * new_screen_height)), int(round((2/45) * new_screen_height)))
        self.rect.size = self.size
        self.texture = pygame.transform.scale(cursor_img, self.size)
    
    def get_position(self):
        return self.position