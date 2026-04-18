import pygame
import random
from bullet import EnemyBullet
import sounds  

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.draw_enemy()
        self.rect = self.image.get_rect()
        self.rect.x = screen_width + random.randint(20, 200)
        self.rect.y = random.randint(40, screen_height - 40)
        
        self.speed = random.randint(3, 6)
        self.shoot_timer = random.randint(30, 90)

    def draw_enemy(self):
        pygame.draw.polygon(self.image, (204, 0, 255),
                           [(2, 6), (10, 12), (18, 6), (26, 12), (18, 18), (10, 16), (2, 22)])
        pygame.draw.rect(self.image, (102, 0, 153), (8, 10, 12, 8), border_radius=3)
        pygame.draw.circle(self.image, (255, 0, 0), (11, 14), 2)
        pygame.draw.circle(self.image, (255, 0, 0), (17, 14), 2)

    def update(self, player, enemy_bullets_group, all_sprites_group):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
            return

        self.shoot_timer -= 1
        if self.shoot_timer <= 0 and player.health > 0:
            self.shoot_timer = random.randint(60, 120)
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery)
            enemy_bullets_group.add(bullet)
            all_sprites_group.add(bullet)
            sounds.enemy_shoot_sound.play()  