import pygame, random, math
from constants import *
from field import Field

class Player:
    def __init__(self, field:Field):
        self.x = field.sidelength // 2  # Startposition des Spielers
        self.y = field.sidelength // 2
        player_sidelength = int(round((5/100) * field.sidelength))
        self.size = (player_sidelength, player_sidelength)  # Größe des Spielers
        self.middle = (self.x + self.size[0] / 2, self.y + self.size[1] / 2) # Create Player Middle
        self.sword_size = int(round(self.size[0])) # Größe des Schwertes
        self.attack_range = pygame.Rect(self.middle[0], self.middle[1], self.sword_size, self.sword_size) # Attack Range of the Player
        self.movespeed = 4 * (field.sidelength/1000)  # Geschwindigkeit des Spielers 
        self.rect = pygame.Rect((round(self.x), round(self.y)), self.size) # Create Player Rectangle
        self.position = (self.x, self.y) # Create Player Position
        self.moving = False # Is the player moving
        self.last_position = (self.x, self.y) # Last position of the player
        self.attacking = False # Is the player attacking
        self.attack_frame = 0 # Frame of the attack animation
        self.last_hit = 0 # Time of the last hit
        self.arrows = [] # List of arrows
        self.health = 1 # Health of the player
        self.kills = 0 # Kills of the player
        self.arrowcount = 0
        self.lastarrow = 0
        
    def move(self, field:Field):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]: 
            if self.x - self.movespeed > 0:
                self.x -= self.movespeed  # Move left
        if key[pygame.K_d]:
            if self.x + self.movespeed < field.sidelength - self.size[0]:
                self.x += self.movespeed  # Move right
        if key[pygame.K_w]:
            if self.y - self.movespeed > 0:
                self.y -= self.movespeed  # Move up
        if key[pygame.K_s]:
            if self.y + self.movespeed < field.sidelength - self.size[1]:
                self.y += self.movespeed  # Move down

        self.position = (self.x, self.y) # Update Player Position
        self.rect.topleft = (round(self.x), round(self.y)) # Update Player Rectangle
        self.middle = (self.x + self.size[0] / 2, self.y + self.size[1] / 2) # Update Player Middle

    def update_for_resize(self, old_fieldlength, new_fieldlength):
        # Update player size
        player_sidelength = int(round((5/100) * new_fieldlength))
        self.size = (player_sidelength, player_sidelength)
        
        # Update player speed
        self.movespeed = 4 * (new_fieldlength/1000)

        # Update player position
        self.x = self.x * new_fieldlength / old_fieldlength
        self.y = self.y * new_fieldlength / old_fieldlength
        self.position = (self.x, self.y)
        self.middle = (self.x + self.size[0] / 2, self.y + self.size[1] / 2)

        # Update player rectangle
        self.rect = pygame.Rect((round(self.x), round(self.y)), self.size)

    def load_texture(self, player_img):
        player_img = pygame.transform.scale(player_img, self.size)

    def draw(self, screen, player_img):
        player_img_rotated = pygame.transform.scale(player_img, self.size) # Scale the player image
        screen.blit(player_img_rotated, (round(self.x), round(self.y))) # Draw Player Model

    # This method calculates the corners of a rectangle that is centered on the player,
    # rotated so that one of its long sides is parallel to the line from the player to the mouse,
    # and has a width 3 times the player's width and the same height as the player.
    def calculate_corners(self, mouse_pos, width, height):
        # Calculate the difference in x and y between the mouse and the player
        dx = mouse_pos[0] - self.middle[0]
        dy = mouse_pos[1] - self.middle[1]
        # Calculate the angle from the player to the mouse, and add 90 degrees
        angle = math.atan2(dy, dx) + math.pi / 2  # Add 90 degrees

        # Calculate half the width and height of the rectangle
        half_width = width / 2
        half_height = height / 2

        # Calculate the translation distance (half the player's size away)
        tx = 2 * self.size[0] / 2 * math.cos(angle - math.pi / 2)
        ty = 2 * self.size[0] / 2 * math.sin(angle - math.pi / 2)

        # Calculate the corners of the rectangle
        corners = []
        for dx, dy in [(-half_width, -half_height), (half_width, -half_height), (half_width, half_height), (-half_width, half_height)]:
            # Rotate and translate the corner relative to the player's position
            x = self.middle[0] + dx * math.cos(angle) - dy * math.sin(angle) + tx
            y = self.middle[1] + dx * math.sin(angle) + dy * math.cos(angle) + ty
            corners.append([x, y])

        # Return the corners of the rectangle
        return corners
    
    # This method checks if any enemies are hit by the player's attack
    def check_hit(self, screen, enemies: list):
        # Initialize the list of hit enemies
        hit = []
        # Calculate the dimensions of the attack range
        width = self.size[0] * 3
        height = self.size[1]
        # Calculate the corners of the attack range
        corners = self.calculate_corners(pygame.mouse.get_pos(), width, height)

        # Draw the attack range on the screen for testing purposes
        # pygame.draw.polygon(screen, (255, 0, 0), corners)
        # pygame.image.save(screen, "Knights_Fury/_images/attack_range.png")
        
        # Create a new surface with the same dimensions as the screen
        surface = pygame.Surface(screen.get_size())
        # Draw the attack range on the new surface
        attack_range = pygame.draw.polygon(surface, (0, 0, 0), corners)

        # Check each enemy for a collision with the attack range
        for idx_enemy, enemy in enumerate(enemies):
            # If the enemy's rectangle collides with the attack range, add it to the hit list
            if attack_range.colliderect(enemy.rect):
                hit.append(idx_enemy)

        # Return the list of hit enemies
        return hit

    def attack(self, screen, enemies: list, mouse_pos: tuple, attacking_status: bool):
        if attacking_status:
            if self.attack_frame == 0:
                self.last_hit = pygame.time.get_ticks()
                self.attack_frame = 1
    
    def calculate_angle(self, mouse_pos: tuple):
        source_pos_vector = pygame.math.Vector2(self.middle)
        target_pos_vector = pygame.math.Vector2(mouse_pos)
        direction = target_pos_vector - source_pos_vector
        angle = math.degrees(math.atan2(direction.x, direction.y))
        return angle