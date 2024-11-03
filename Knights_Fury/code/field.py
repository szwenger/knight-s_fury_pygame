import pygame, random, math
from constants import *

# Field Class

class Field:
    def __init__(self):
        self.size = (720, 720)
        self.sidelength = self.size[0]
        self.rect = pygame.Rect((0, 0), self.size)
        self.middle = (self.sidelength / 2, self.sidelength / 2)
        self.background = pygame.transform.scale(background_1_img, self.size)
        
    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        
    def update_for_resize(self, new_screen_height):
        self.size = (new_screen_height, new_screen_height)
        self.rect.size = self.size
        self.sidelength = new_screen_height
        self.rect = pygame.Rect((0, 0), self.size)
        self.background = pygame.transform.scale(background_1_img, self.size)
        
    def obstacle_collide(self, player):
        if player.rect.colliderect(self.rect):
            return True
        return False