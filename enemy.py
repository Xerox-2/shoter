import pygame
import random
from bullet import EnemyBullet
from assets_loader import assets
import sounds

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Оригинальный враг (без двигателя)
        self.base_ship = assets.enemy_ship
        self.rect = self.base_ship.get_rect()
        self.rect.x = screen_width + random.randint(20, 200)
        self.rect.y = random.randint(40, screen_height - 40)
        
        self.speed = random.randint(3, 6)
        self.shoot_timer = random.randint(30, 90)
        
        # Анимация двигателя
        self.trail_frame = 0
        self.trail_timer = 0
        
        # Размер врага фиксированный
        self.ship_width = self.base_ship.get_width()
        self.ship_height = self.base_ship.get_height()
        
        # Создаём изображение с двигателем
        self.update_ship_image()

    def update_ship_image(self):
        """Обновляет изображение врага с анимацией двигателя"""
        # Чередуем кадры двигателя
        if self.trail_frame < 10:
            trail = assets.enemy_trail
        else:
            trail = assets.enemy_trail_flip
        
        # Создаём поверхность (ширина = корабль + двигатель)
        full_image = pygame.Surface((self.ship_width + trail.get_width(),
                                     max(self.ship_height, trail.get_height() + 4)),  # +4 для дополнительного места
                                    pygame.SRCALPHA)
        
        # Рисуем корабль (слева, двигатель будет справа)
        full_image.blit(self.base_ship, (0, full_image.get_height()//2 - self.ship_height//2))
        
        # Рисуем двигатель справа от корабля 
        trail_y = full_image.get_height()//2 - trail.get_height()//2 + 2  
        full_image.blit(trail, (self.ship_width, trail_y))
        
        # Сохраняем изображение
        self.image = full_image

    def update(self, player, enemy_bullets_group, all_sprites_group):
        # Сохраняем старую позицию
        old_center = self.rect.center
        
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
            return
        
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

        if player and player.alive():
            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                self.shoot_timer = random.randint(60, 120)
                bullet = EnemyBullet(self.rect.centerx, self.rect.centery)
                enemy_bullets_group.add(bullet)
                all_sprites_group.add(bullet)
                sounds.enemy_shoot_sound.play()