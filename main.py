import pygame
import random
from player import Player
from enemy import Enemy
from star import Star
from bullet import Bullet, EnemyBullet
import sounds

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scroll Shooter")
clock = pygame.time.Clock()

def reset_game():
    """Сбрасывает игру в начальное состояние"""
    global all_sprites, enemies, bullets, enemy_bullets, stars
    global player, score, running
    
    # Очищаем все группы
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    stars = pygame.sprite.Group()
    
    # Создаём фон из звёзд
    for _ in range(100):
        star = Star(WIDTH, HEIGHT)
        stars.add(star)
        all_sprites.add(star)
    
    # Создаём игрока
    player = Player(WIDTH, HEIGHT)
    all_sprites.add(player)
    
    # Сбрасываем счёт
    score = 0
    
    # Останавливаем все звуки
    pygame.mixer.stop()

def show_game_over():
    """Показывает экран Game Over и ждёт рестарта"""
    global running
    
    # Останавливаем игровые звуки
    pygame.mixer.stop()
    sounds.game_over_sound.play()
    
    font = pygame.font.Font(None, 36)
    go_font = pygame.font.Font(None, 72)
    small_font = pygame.font.Font(None, 28)
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # ← РЕСТАРТ ПО R
                    waiting = False
                    reset_game()
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False
        
        # Отрисовка Game Over экрана
        screen.fill((5, 5, 20))
        
        go_text = go_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(go_text, (WIDTH//2 - 150, HEIGHT//2 - 80))
        
        score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH//2 - 100, HEIGHT//2 - 20))
        
        restart_text = small_font.render("Press R to Restart", True, (150, 150, 150))
        screen.blit(restart_text, (WIDTH//2 - 90, HEIGHT//2 + 30))
        
        quit_text = small_font.render("Press ESC to Quit", True, (150, 150, 150))
        screen.blit(quit_text, (WIDTH//2 - 90, HEIGHT//2 + 60))
        
        pygame.display.flip()
        clock.tick(60)
    
    return True

# Инициализация игры
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
stars = pygame.sprite.Group()

for _ in range(100):
    star = Star(WIDTH, HEIGHT)
    stars.add(star)
    all_sprites.add(star)

player = Player(WIDTH, HEIGHT)
all_sprites.add(player)

score = 0
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Таймер спавна врагов
ENEMY_SPAWN = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_SPAWN, 1200)

# Основной игровой цикл
running = True
game_active = True

while running:
    if game_active:
        # --- Активная игра ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == ENEMY_SPAWN:
                enemy = Enemy(WIDTH, HEIGHT)
                enemies.add(enemy)
                all_sprites.add(enemy)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = player.shoot()
                    if bullet:
                        bullets.add(bullet)
                        all_sprites.add(bullet)
                        sounds.shoot_sound.play()
                elif event.key == pygame.K_r:  # ← РЕСТАРТ В ЛЮБОЙ МОМЕНТ
                    reset_game()
                    pygame.time.set_timer(ENEMY_SPAWN, 1200)  # перезапускаем таймер

        keys = pygame.key.get_pressed()
        player.update(keys)
        
        for sprite in all_sprites:
            if isinstance(sprite, Enemy):
                sprite.update(player, enemy_bullets, all_sprites)
            elif isinstance(sprite, (Star, Bullet, EnemyBullet)):
                sprite.update()

        # Столкновения пуль с врагами
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 100
            sounds.explosion_sound.play()
            enemy = Enemy(WIDTH, HEIGHT)
            enemies.add(enemy)
            all_sprites.add(enemy)

        # Столкновения вражеских пуль с игроком
        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        if hits:
            player.health -= 1
            sounds.hit_sound.play()
            if player.health <= 0:
                game_active = False

        # Столкновения игрока с врагами
        hits = pygame.sprite.spritecollide(player, enemies, True)
        if hits:
            player.health -= len(hits)
            sounds.hit_sound.play()
            if player.health <= 0:
                game_active = False

        # Отрисовка
        screen.fill((5, 5, 20))
        all_sprites.draw(screen)

        # Интерфейс
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        health_text = font.render(f"Health: {player.health}", True, (255, 100, 100))
        screen.blit(health_text, (10, 50))
        
        # Подсказка
        hint_text = small_font.render("R - Restart", True, (100, 100, 100))
        screen.blit(hint_text, (WIDTH - 120, 10))

        pygame.display.flip()
        clock.tick(60)
    
    else:
        # --- Game Over ---
        if show_game_over():
            game_active = True
            pygame.time.set_timer(ENEMY_SPAWN, 1200)
        else:
            running = False

pygame.quit()