import pygame

class Assets:
    def __init__(self):
        # Загружаем спрайт-листы
        self.ships_sheet = pygame.image.load('img/SpaceShooterAssetPack_Ships.png')
        self.projectiles_sheet = pygame.image.load('img/SpaceShooterAssetPack_Projectiles.png')
        self.misc_sheet = pygame.image.load('img/SpaceShooterAssetPack_Miscellaneous.png')
        self.hearts_sheet = pygame.image.load('img/SpaceShooterAssetPack_hearts.png')
        
        # --- КОРАБЛИ (из Ships.png) ---
        self.player_ship = self._get_sprite(self.ships_sheet, 48, 16, 15, 15)
        self.enemy_ship = self._get_sprite(self.ships_sheet, 32, 64, 7, 7)
        
        # --- ПУЛИ (из Projectiles.png) ---
        self.bullet = self._get_sprite(self.projectiles_sheet, 0, 65, 48, 15)
        self.enemy_bullet = self._get_sprite(self.projectiles_sheet, 24, 73, 23, 5)
        
        # --- СЕРДЕЧКИ (из hearts.png) ---
        self.heart_full = self._get_sprite(self.hearts_sheet, 440, 740, 160, 140)
        self.heart_empty = self._get_sprite(self.hearts_sheet, 1060, 740, 160, 140)
        
        # --- СЛЕДЫ/ДВИГАТЕЛИ (из Miscellaneous.png) ---
        # След игрока (оригинал - смотрит вверх)
        player_trail_orig = self._get_sprite(self.misc_sheet, 42, 24, 3, 4)
        # Поворачиваем на 90 градусов (чтобы смотрел вправо)
        self.player_trail = pygame.transform.rotate(player_trail_orig, -90)
        
        # След игрока отзеркаленный
        player_trail_flip_orig = self._get_sprite(self.misc_sheet, 50, 24, 3, 4)
        self.player_trail_flip = pygame.transform.rotate(player_trail_flip_orig, -90)
        
        # След врага (оригинал - смотрит вверх)
        enemy_trail_orig = self._get_sprite(self.misc_sheet, 90, 24, 3, 3)
        # Поворачиваем на 90 градусов
        self.enemy_trail = pygame.transform.rotate(enemy_trail_orig, -90)
        
        # След врага отзеркаленный
        enemy_trail_flip_orig = self._get_sprite(self.misc_sheet, 98, 24, 3, 4)
        self.enemy_trail_flip = pygame.transform.rotate(enemy_trail_flip_orig, -90)
        
        # --- ВЗРЫВЫ ---
        self.explosion1 = self._get_sprite(self.misc_sheet, 97, 57, 5, 5)
        self.explosion2 = self._get_sprite(self.misc_sheet, 88, 56, 7, 7)
        self.explosion3 = self._get_sprite(self.misc_sheet, 80, 56, 7, 7)
        self.explosion4 = self._get_sprite(self.misc_sheet, 75, 59, 1, 1)
        
        self.enemy_explosion1 = self._get_sprite(self.misc_sheet, 65, 49, 5, 5)
        self.enemy_explosion2 = self._get_sprite(self.misc_sheet, 56, 48, 7, 7)
        self.enemy_explosion3 = self._get_sprite(self.misc_sheet, 48, 48, 7, 7)
        self.enemy_explosion4 = self._get_sprite(self.misc_sheet, 43, 51, 1, 1)
        
        # Масштабируем
        self.player_ship = pygame.transform.scale(self.player_ship, (40, 40))
        self.enemy_ship = pygame.transform.scale(self.enemy_ship, (35, 35))
        
        self.bullet = pygame.transform.scale(self.bullet, (20, 8))
        self.enemy_bullet = pygame.transform.scale(self.enemy_bullet, (15, 5))
        
        self.heart_full = pygame.transform.scale(self.heart_full, (30, 27))
        self.heart_empty = pygame.transform.scale(self.heart_empty, (30, 27))
        
        # Масштабируем следы (делаем их чуть крупнее)
        self.player_trail = pygame.transform.scale(self.player_trail, (8, 10))
        self.player_trail_flip = pygame.transform.scale(self.player_trail_flip, (8, 10))
        self.enemy_trail = pygame.transform.scale(self.enemy_trail, (8, 8))
        self.enemy_trail_flip = pygame.transform.scale(self.enemy_trail_flip, (8, 10))
        
        # Собираем анимацию взрыва
        self.explosion_frames = [
            pygame.transform.scale(self.explosion1, (20, 20)),
            pygame.transform.scale(self.explosion2, (25, 25)),
            pygame.transform.scale(self.explosion3, (30, 30)),
            pygame.transform.scale(self.explosion4, (15, 15))
        ]
        
        self.enemy_explosion_frames = [
            pygame.transform.scale(self.enemy_explosion1, (20, 20)),
            pygame.transform.scale(self.enemy_explosion2, (25, 25)),
            pygame.transform.scale(self.enemy_explosion3, (30, 30)),
            pygame.transform.scale(self.enemy_explosion4, (15, 15))
        ]
    
    def _get_sprite(self, sheet, x, y, width, height):
        """Вырезает спрайт из спрайт-листа"""
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(sheet, (0, 0), (x, y, width, height))
        return sprite

assets = Assets()