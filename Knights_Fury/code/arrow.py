import pygame, random, math
from constants import *
from field import Field

class Arrow:
    def __init__(self, x, y, angle, speed, damage, image, field: Field):
        self.x = x
        self.y = y
        self.angle = angle
        self.side_lenght = (1/45) * field.sidelength
        self.speed = speed
        self.damage = damage
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.side_lenght, self.side_lenght))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.isDrawn = False
        
    def move(self):
        radian_angle = math.radians(self.angle - 90)
        self.x += self.speed * math.cos(radian_angle)
        self.y -= self.speed * math.sin(radian_angle)
        self.rect.center = (self.x, self.y)
        
    def draw(self, screen):
        self.isDrawn = True
        screen.blit(self.image, self.rect)
        
    def check_Collision_enemy(self, enemy):
        return self.rect.colliderect(enemy.rect)
    
    def check_Collision_player(self, player):
        return self.rect.colliderect(player.rect)
    
    def checkOffScreen(self, field_len):
        return self.x < 0 or self.x > field_len or self.y < 0 or self.y > field_len
    
    def update_for_resize(self, old_fieldlenght, field: Field):
        self.side_lenght = (1/45) * field.sidelength
        self.image = pygame.transform.scale(self.image, (self.side_lenght, self.side_lenght))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
    