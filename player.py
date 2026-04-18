import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Создаём поверхность и рисуем корабль
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.draw_ship()
        self.rect = self.image.get_rect()
        self.rect.center = (100, screen_height // 2)
        
        self.speed = 6
        self.health = 5
        self.shoot_cooldown = 0
        self.shoot_delay = 15  # кадров между выстрелами

    def draw_ship(self):
        # Корпус (стрела)
        pygame.draw.polygon(self.image, (0, 212, 255), 
                           [(8, 8), (28, 16), (8, 24)])
        # Крылья
        pygame.draw.polygon(self.image, (0, 136, 204),
                           [(12, 4), (16, 4), (10, 16), (16, 28), (12, 28), (6, 16)])
        # Кабина
        pygame.draw.circle(self.image, (224, 255, 255), (18, 16), 3)
        # Двигатель (огонь)
        pygame.draw.polygon(self.image, (255, 102, 0),
                   [(2, 12), (6, 12), (4, 8)])   # верхний язык
        pygame.draw.polygon(self.image, (255, 102, 0),
                   [(2, 20), (6, 20), (4, 24)])  # нижний язык

    def update(self, keys):
        # Движение
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        # Границы экрана
        self.rect.clamp_ip(pygame.Rect(0, 0, self.screen_width, self.screen_height))

        # Кулдаун стрельбы
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = self.shoot_delay
            return Bullet(self.rect.right, self.rect.centery)
        return None