import pygame

class Bullet(pygame.sprite.Sprite):
    """Пуля игрока"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 6), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (0, 255, 204), (0, 1, 16, 4))
        pygame.draw.rect(self.image, (255, 255, 255), (0, 2, 6, 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 12

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > 900:  # за экраном
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    """Пуля врага"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((14, 14), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 51, 0), (7, 7), 6)
        pygame.draw.circle(self.image, (255, 255, 0), (5, 5), 2)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -8

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < -100:
            self.kill()