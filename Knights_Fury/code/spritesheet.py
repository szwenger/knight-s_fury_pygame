import pygame

pygame.init()

pygame.display.set_mode((1280, 720))

# ---------- Sprite Sheet Class ----------

class SpriteSheet:
    def __init__ (self, image):
        self.sheet = image
        
    def get_image(self, frame, width, height, scale):
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        
        return image