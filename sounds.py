import pygame
import math
import io
import wave
import struct

# Инициализация микшера
pygame.mixer.init(frequency=22050, size=-16, channels=2)

def generate_sound(frequency, duration, volume=0.3):
    """Генерирует звук через создание WAV в памяти"""
    sample_rate = 22050
    num_samples = int(sample_rate * duration)
    
    # Создаём WAV файл в памяти
    wav_buffer = io.BytesIO()
    
    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)  # моно
        wav_file.setsampwidth(2)  # 16 бит
        wav_file.setframerate(sample_rate)
        
        # Генерируем сэмплы
        for i in range(num_samples):
            t = float(i) / sample_rate
            value = math.sin(2.0 * math.pi * frequency * t)
            
            # Затухание для более длинных звуков
            if duration > 0.15:
                fade = 1.0 - (i / num_samples)
                value *= fade
            
            # Конвертируем в 16-бит signed integer
            sample = int(value * volume * 32767)
            
            # Записываем как little-endian 16-bit
            wav_file.writeframes(struct.pack('<h', sample))
    
    # Создаём Sound из буфера
    wav_buffer.seek(0)
    return pygame.mixer.Sound(wav_buffer)

# Создаём звуки
shoot_sound = generate_sound(780, 0.05, 0.06)        # выстрел игрока
enemy_shoot_sound = generate_sound(440, 0.06, 0.04)   # выстрел врага
hit_sound = generate_sound(220, 0.1, 0.3)            # попадание
explosion_sound = generate_sound(110, 0.25, 0.15)    # взрыв врага
game_over_sound = generate_sound(220, 0.5, 0.15)     # проигрыш

# Фоновая музыка пока None
bg_music = None