# explosion.py
import pygame
from assets_loader import assets

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, is_player=True):
        super().__init__()
        if is_player:
            self.frames = assets.explosion_frames
        else:
            self.frames = assets.enemy_explosion_frames
        
        self.current_frame = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.animation_speed = 0.1  # секунд на кадр
        self.last_update = pygame.time.get_ticks()
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.kill()  # удаляем взрыв после анимации
            else:
                self.image = self.frames[self.current_frame]