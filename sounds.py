import pygame
import os

# Инициализация микшера
pygame.mixer.init(frequency=44100, size=-16, channels=2)

# Путь к папке со звуками
AUDIO_PATH = os.path.join(os.path.dirname(__file__), "audio")

def load_sound(filename, volume=1.0):
    """Загружает звук из файла с регулировкой громкости"""
    path = os.path.join(AUDIO_PATH, filename)
    if os.path.exists(path):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        return sound
    else:
        print(f" Файл не найден: {path}")
        return None

# Загружаем звуки
shoot_sound = load_sound("laser1.ogg", 0.1)           # выстрел игрока
enemy_shoot_sound = load_sound("laser2.ogg", 0.02)     # выстрел врага
hit_sound = load_sound("hpdown.ogg", 0.2)             # потеря HP
explosion_sound = load_sound("explosion.ogg", 0.05)    # взрыв врага
game_over_sound = load_sound("gameOver.ogg", 0.15)     # проигрыш

# Фоновая музыка (если будет)
bg_music = None
music_loaded = False

def load_background_music(filename="bg_music.ogg", volume=0.3):
    """Загружает и запускает фоновую музыку"""
    global bg_music, music_loaded
    path = os.path.join(AUDIO_PATH, filename)
    if os.path.exists(path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1, fade_ms=2000)  # бесконечный цикл
        music_loaded = True
        print(" Фоновая музыка запущена")
    else:
        print(f" Фоновая музыка не найдена: {path}")
        print("  Игра будет без фоновой музыки")

def stop_music():
    """Останавливает фоновую музыку"""
    pygame.mixer.music.fadeout(500)