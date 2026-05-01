import pygame
from assets_loader import assets

class Bullet(pygame.sprite.Sprite):
    """Пуля игрока"""
    def __init__(self, x, y):
        super().__init__()
        self.image = assets.bullet
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 12

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > 900:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    """Пуля врага"""
    def __init__(self, x, y):
        super().__init__()
        self.image = assets.enemy_bullet
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -8

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < -100:
            self.kill()