import pygame
from bullet import Bullet
from assets_loader import assets

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Оригинальный корабль (без двигателя)
        self.base_ship = assets.player_ship
        self.rect = self.base_ship.get_rect()
        self.rect.center = (100, screen_height // 2)
        
        self.speed = 6
        self.health = 5
        self.shoot_cooldown = 0
        self.shoot_delay = 15
        
        # Анимация двигателя
        self.trail_frame = 0
        self.trail_timer = 0
        
        # Размер корабля фиксированный
        self.ship_width = self.base_ship.get_width()
        self.ship_height = self.base_ship.get_height()
        
        # Создаём изображение с двигателем
        self.update_ship_image()

    def update_ship_image(self):
        """Обновляет изображение корабля с анимацией двигателя"""
        # Чередуем кадры двигателя
        if self.trail_frame < 10:
            trail = assets.player_trail
        else:
            trail = assets.player_trail_flip
        
        # Создаём поверхность (ширина = корабль + двигатель)
        full_image = pygame.Surface((self.ship_width + trail.get_width(), 
                                     max(self.ship_height, trail.get_height())), 
                                    pygame.SRCALPHA)
        
        # Рисуем корабль 
        full_image.blit(self.base_ship, (trail.get_width(), 
                                         full_image.get_height()//2 - self.ship_height//2))
        # Рисуем двигатель  слева от корабля
        full_image.blit(trail, (0, full_image.get_height()//2 - trail.get_height()//2))
        
        # Сохраняем изображение
        self.image = full_image

    def update(self, keys):
        # Сохраняем старую позицию
        old_center = self.rect.center
        
        # Движение
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        # Границы
        self.rect.clamp_ip(pygame.Rect(0, 0, self.screen_width, self.screen_height))

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # Анимация двигателя
        self.trail_timer += 1
        if self.trail_timer > 5:
            self.trail_timer = 0
            self.trail_frame += 1
            if self.trail_frame > 19:
                self.trail_frame = 0
            self.update_ship_image()
            # Восстанавливаем позицию
            self.rect.center = old_center

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = self.shoot_delay
            return Bullet(self.rect.right, self.rect.centery)
        return None