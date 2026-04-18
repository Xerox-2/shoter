import pygame
import random

class Star(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        size = random.randint(1, 3)
        self.image = pygame.Surface((size, size))
        brightness = random.randint(100, 255)
        self.image.fill((brightness, brightness, brightness))
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width)
        self.rect.y = random.randint(0, screen_height)
        
        self.speed = random.uniform(0.5, 2.5)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = self.screen_width
            self.rect.y = random.randint(0, self.screen_height)