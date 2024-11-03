import pygame, random, math
from constants import *
from field import *
import time

# Enemy Class
class Enemy:
    def __init__(self, size, speed, weaponsize, attackrange, field:Field):
        #Choose random Spawn-Area
        spawn = random.randint(1,4) # Random Spawn
        if spawn == 1: #top
            self.x = 1*random.randint(0,field.sidelength)
            self.y = -1*random.randint(0,int(round(0.2 * field.sidelength)))
        elif spawn == 2: #bottom
            self.x = 1*random.randint(0,field.sidelength)
            self.y = 1*(random.randint(field.sidelength,int(round(1.2 * field.sidelength)))) 
        elif spawn == 3:#left
            self.x = -1*random.randint(0,int(round(0.2 * field.sidelength))) 
            self.y = 1*random.randint(0,field.sidelength)
        elif spawn == 4: #right
            self.x = 1*(random.randint(field.sidelength,int(round(1.2 * field.sidelength))))
            self.y = 1*random.randint(0,field.sidelength)
            
        self.relative_size = size
        self.size = (int(round((self.relative_size/100) * field.sidelength)), int(round((self.relative_size/100) * field.sidelength)))
        self.relative_speed = speed
        self.speed = speed * (field.sidelength/1000) 
        self.is_attacking = False
        self.last_attack_time = 0
        self.rect = pygame.Rect((self.x, self.y), self.size )  
        self.middle = (self.x + self.size[0] / 2, self.y + self.size[1] / 2)
        self.hitplayer = False
        self.relative_weaponsize = weaponsize
        self.weaponsize = int(round((self.relative_weaponsize/1000) * field.sidelength))
        self.relative_attackrange = attackrange
        self.attackrange = int(round((self.relative_attackrange/1000) * field.sidelength))
        
        


    def get_direction(self, player_pos):
        dx = player_pos[0] - self.x  # Berechne den x-Abstand zum Spieler
        dy = player_pos[1] - self.y  # Berechne den y-Abstand zum Spieler
        distance = math.sqrt(dx**2+dy**2)  # Berechne die Entfernung zum Spieler
        direction_x = dx / distance  # Normalisiere den x-Abstand
        direction_y = dy / distance  # Normalisiere den y-Abstand
        return direction_x, direction_y  # Gebe die Richtung zum Spieler zurück

    def enemycollide(self, enemies):
        for other_enemy in enemies:
            if self is not other_enemy and self.rect.colliderect(other_enemy.rect):
                # Calculate the direction to move the enemy away
                dx = self.x - other_enemy.x
                dy = self.y - other_enemy.y
                distance = math.sqrt(dx**2 + dy**2)

                # Move the enemy away a little bit
                self.x += dx / distance
                self.y += dy / distance

                # Update the rect property of the enemy after the position change
                self.rect.topleft = (round(self.x), round(self.y))
        
    def inAttackRange(self, player_pos):
        dx = player_pos[0] - self.x  # Berechne den x-Abstand zum Spieler
        dy = player_pos[1] - self.y  # Berechne den y-Abstand zum Spieler
        distance = math.sqrt(dx**2+dy**2)  # Berechne die Entfernung zum Spieler
        if distance < self.attackrange:
            return True
        return False
    
    def attack(self, rect: pygame.Rect):
        weapon = pygame.Rect(self.x, self.y, self.weaponsize, self.weaponsize)
        if weapon.colliderect(rect):
            print("HIT HIT HIT")
            self.hitplayer =True

    def update(self, player_pos, rect : pygame.Rect, speed, enemies):
        if self.is_attacking:  # If the enemy is attacking
            if pygame.time.get_ticks() - self.last_attack_time > self.delay:  # If the attack delay has passed
                if self.type == "melee":
                    self.attack(rect)  # Per form the attack
                    self.is_attacking = False  # Reset the attacking state
        else:  # If the enemy is not attacking
            direction_x, direction_y = self.get_direction(player_pos)  # Get the direction to the player

            self.x += direction_x * speed  # Update the x position of the enemy
            self.y += direction_y * speed  # Update the y position of the enemy

            self.rect.topleft = (round(self.x), round(self.y))  # Update the position of the enemy's rectangle
            
            self.enemycollide(enemies) # Check for collision with other enemies
            
            if self.inAttackRange(player_pos):  # If the enemy is in range to attack
                self.is_attacking = True  # Set the attacking state
                self.last_attack_time = pygame.time.get_ticks()  # Set the last attack time to the current time
        self.middle = (self.x + self.size[0] / 2, self.y + self.size[1] / 2) # Update the middle of the enemy

    def update_for_resize(self, field: Field, old_fieldlength: int, new_screen_width: int):
        self.size = (int(round((self.relative_size/100) * field.sidelength)), int(round((self.relative_size/100) * field.sidelength)))
        self.rect.size = self.size
        self.speed = self.relative_speed * (field.sidelength/1000)
        self.x = min(self.x * (field.sidelength/old_fieldlength), new_screen_width - self.size[0])
        self.y = min(self.y * (field.sidelength/old_fieldlength), field.sidelength - self.size[1])
        self.middle = (self.x + self.size[0] / 2, self.y + self.size[1] / 2)

        self.weaponsize = int(round((self.relative_weaponsize/1000) * field.sidelength))
        self.attackrange = int(round((self.relative_attackrange/1000) * field.sidelength))

        self.rect = pygame.Rect((round(self.x), round(self.y)), self.size)
           

            
      

class SmallGoblin(Enemy):
    def __init__(self, field):
        self.speed = 3  
        self.size = 3 
        self.delay = 400
        self.health = 1
        self.weaponsize = 45
        self.attackrange = 35
        self.type = "melee"
        super().__init__(self.size, self.speed, self.weaponsize, self.attackrange, field)  

class Orc(Enemy):
    def __init__(self, field):
        self.speed = 2  
        self.size = 5 
        self.delay =650
        self.health = 2
        self.weaponsize = 65
        self.attackrange = 55
        self.type = "melee"

        super().__init__(self.size, self.speed, self.weaponsize, self.attackrange, field)   

class Ogre(Enemy):
    def __init__(self, field):
        self.speed = 1  
        self.size = 10 
        self.delay = 800
        self.health = 4
        self.weaponsize = 150
        self.attackrange = 100
        self.type = "melee"
        super().__init__(self.size, self.speed, self.weaponsize, self.attackrange, field)  

class archer(Enemy):
    def __init__(self, field):
        self.speed = 2  
        self.size = 3 
        self.delay = 2000
        self.health = 1
        self.weaponsize = 30
        self.attackrange = 400
        self.type = "ranged"
        super().__init__(self.size, self.speed, self.weaponsize, self.attackrange, field)  
        self.arrows = [] 
        
    def calculate_angle_to_player(self, player_pos: tuple):
        source_pos_vector = pygame.math.Vector2(self.middle)
        target_pos_vector = pygame.math.Vector2(player_pos)
        direction = target_pos_vector - source_pos_vector
        angle = math.degrees(math.atan2(direction.x, direction.y))
        return angle






class petwolf():
    ...