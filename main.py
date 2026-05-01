import pygame
import random
from player import Player
from enemy import Enemy
from star import Star
from bullet import Bullet, EnemyBullet
from assets_loader import assets
from explosion import Explosion
import sounds

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scroll Shooter")
clock = pygame.time.Clock()

def reset_game():
    """Сбрасывает игру в начальное состояние"""
    global all_sprites, enemies, bullets, enemy_bullets, stars, explosions
    global player, score, running, game_active, death_timer
    
    # Очищаем все группы
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    stars = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    
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
    game_active = True
    death_timer = 0
    
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
                if event.key == pygame.K_r:
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
explosions = pygame.sprite.Group()

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
death_timer = 0

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
                elif event.key == pygame.K_r:
                    reset_game()
                    pygame.time.set_timer(ENEMY_SPAWN, 1200)

        keys = pygame.key.get_pressed()
        if player.alive():
            player.update(keys)
        
        # Обновляем всех спрайтов
        for sprite in all_sprites:
            if isinstance(sprite, Enemy):
                if player.alive():
                    sprite.update(player, enemy_bullets, all_sprites)
                else:
                    sprite.update(None, enemy_bullets, all_sprites)
            elif isinstance(sprite, (Star, Bullet, EnemyBullet, Explosion)):
                sprite.update()

        # Столкновения пуль с врагами
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 100
            sounds.explosion_sound.play()
            # Создаём взрыв на месте врага
            explosion = Explosion(hit.rect.centerx, hit.rect.centery, is_player=False)
            explosions.add(explosion)
            all_sprites.add(explosion)

        # Столкновения вражеских пуль с игроком
        if player.alive():
            hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
            if hits:
                player.health -= len(hits)
                sounds.hit_sound.play()
                if player.health <= 0:
                    # Взрыв игрока
                    player_explosion = Explosion(player.rect.centerx, player.rect.centery, is_player=True)
                    explosions.add(player_explosion)
                    all_sprites.add(player_explosion)
                    player.kill()
                    game_active = False
                    death_timer = pygame.time.get_ticks()

        # Столкновения игрока с врагами
        if player.alive():
            hits = pygame.sprite.spritecollide(player, enemies, True)
            if hits:
                player.health -= len(hits)
                sounds.hit_sound.play()
                for hit in hits:
                    # Взрыв на месте врага
                    explosion = Explosion(hit.rect.centerx, hit.rect.centery, is_player=False)
                    explosions.add(explosion)
                    all_sprites.add(explosion)
                if player.health <= 0:
                    player_explosion = Explosion(player.rect.centerx, player.rect.centery, is_player=True)
                    explosions.add(player_explosion)
                    all_sprites.add(player_explosion)
                    player.kill()
                    game_active = False
                    death_timer = pygame.time.get_ticks()

        # Отрисовка
        screen.fill((5, 5, 20))
        all_sprites.draw(screen)

        # Интерфейс
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Сердечки (только если игрок жив)
        if player.alive():
            heart_spacing = 35
            for i in range(player.health):
                screen.blit(assets.heart_full, (10 + i * heart_spacing, 50))
        
        # Подсказка
        hint_text = small_font.render("R - Restart", True, (100, 100, 100))
        screen.blit(hint_text, (WIDTH - 120, 10))

        pygame.display.flip()
        clock.tick(60)
    
    else:
        # --- Game Over с задержкой для анимации взрыва ---
        # Обновляем взрывы
        for sprite in explosions:
            sprite.update()
        
        # Отрисовываем фон и взрывы
        screen.fill((5, 5, 20))
        
        # Рисуем звёзды
        for star in stars:
            screen.blit(star.image, star.rect)
        
        # Рисуем взрывы
        for explosion in explosions:
            screen.blit(explosion.image, explosion.rect)
        
        # Показываем счёт
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Показываем надпись "WAITING..."
        wait_text = small_font.render("WAITING...", True, (200, 200, 200))
        screen.blit(wait_text, (WIDTH//2 - 40, HEIGHT//2))
        
        pygame.display.flip()
        
        # Ждём 1 секунду, пока анимация взрыва закончится
        if pygame.time.get_ticks() - death_timer > 1000:
            if show_game_over():
                game_active = True
                explosions.empty()
                pygame.time.set_timer(ENEMY_SPAWN, 1200)
            else:
                running = False
        
        clock.tick(60)

pygame.quit()