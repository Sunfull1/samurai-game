import pygame
import sys
import os
import math
import random
sys.path.append('.')
from src.constants import *
from src.ui.button import Button

class WinScreen:
    def __init__(self):
        self.retry_button = Button(WIDTH//2 - 125, HEIGHT//2 + 100, 250, 60, "ИГРАТЬ СНОВА", GREEN)
        self.win_font = pygame.font.Font(None, 84)
        self.score_font = pygame.font.Font(None, 48)
        self.message_font = pygame.font.Font(None, 36)
        
        # Параметры для анимации
        self.animation_timer = 0
        self.particles = []
        self.create_particles()
        
        # Загружаем фон (если есть)
        try:
            bg_path = os.path.join('images', 'backgrownd.jpg')
            self.background = pygame.image.load(bg_path)
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
            self.has_bg = True
        except:
            self.has_bg = False
        
        # Эффект тонких лучей для минималистичного дизайна
        self.rays = []
        for i in range(5):  # Еще меньше лучей для минимализма
            angle = i * (math.pi * 2) / 5
            self.rays.append({
                'angle': angle,
                'length': random.randint(80, 150)  # Еще меньше длина для минимализма
            })
    
    def create_particles(self):
        """Создаем частицы для эффекта 'фейерверка' победы"""
        self.particles = []
        for _ in range(15):  # Совсем мало частиц для минимализма
            x = random.randint(WIDTH//3, WIDTH*2//3)
            y = random.randint(HEIGHT//6, HEIGHT//3)
            dx = random.uniform(-1.0, 1.0)
            dy = random.uniform(-1.5, 0)
            color = random.choice([GOLD, (255, 255, 255)])
            size = random.randint(1, 2)  # Маленький размер для минимализма
            lifetime = random.randint(20, 50)
            self.particles.append({
                'x': x, 'y': y, 
                'dx': dx, 'dy': dy,
                'color': color, 'size': size,
                'lifetime': lifetime
            })
    
    def update_particles(self):
        """Обновляем положение частиц"""
        new_particles = []
        for p in self.particles:
            p['lifetime'] -= 1
            if p['lifetime'] > 0:
                # Эффект гравитации
                p['dy'] += 0.05
                p['x'] += p['dx']
                p['y'] += p['dy']
                new_particles.append(p)
        self.particles = new_particles
        
        # Добавляем новые частицы, если старые исчезли
        if len(self.particles) < 5 and random.random() < 0.08:
            self.create_particles()
    
    def draw(self, screen, score):
        # Обновляем анимацию
        self.animation_timer += 0.05
        self.update_particles()
        
        # Рисуем фон
        if self.has_bg:
            # Если есть изображение фона, делаем его немного темнее для контраста
            darkened_bg = self.background.copy()
            dark_overlay = pygame.Surface((WIDTH, HEIGHT))
            dark_overlay.fill((0, 0, 30))
            dark_overlay.set_alpha(100)
            darkened_bg.blit(dark_overlay, (0, 0))
            screen.blit(darkened_bg, (0, 0))
        else:
            # Минималистичный градиент
            for y in range(HEIGHT):
                blue_value = max(0, 30 - y // 20)
                pygame.draw.line(screen, (0, 0, blue_value), (0, y), (WIDTH, y))
        
        # Создаем тонкие линии для минималистичного дизайна
        for i in range(0, WIDTH, 40):  # Больше расстояние между линиями для минимализма
            alpha = 15 + 10 * math.sin((self.animation_timer + i/200) * 0.5)
            pygame.draw.line(screen, (255, 215, 0, int(alpha)), 
                          (i, 0), (i, HEIGHT), 1)
        
        # Рисуем минималистичные световые лучи (делаем их еще тоньше и прозрачнее)
        ray_center_x, ray_center_y = WIDTH // 2, HEIGHT // 3 - 80  # Источник лучей еще выше
        ray_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        for ray in self.rays:
            # Уменьшаем длину и яркость лучей для минимализма
            length = (ray['length'] * 0.4) + math.sin(self.animation_timer) * 3
            end_x = ray_center_x + math.cos(ray['angle'] + self.animation_timer * 0.03) * length
            end_y = ray_center_y + math.sin(ray['angle'] + self.animation_timer * 0.03) * length
            
            # Рисуем более тонкие лучи с еще меньшей непрозрачностью
            pygame.draw.line(ray_surface, (255, 215, 0, 5), 
                          (ray_center_x, ray_center_y), 
                          (end_x, end_y), 1)
        
        screen.blit(ray_surface, (0, 0))
        
        # Создаем эффект пульсации для текста
        title_scale = 1.0 + 0.04 * math.sin(self.animation_timer * 0.08)
        
        # Рисуем текст победы (Более крупный и выразительный)
        win_text = self.win_font.render("ПОБЕДА!", True, GOLD)
        # Масштабируем текст
        scaled_width = int(win_text.get_width() * title_scale)
        scaled_height = int(win_text.get_height() * title_scale)
        scaled_win_text = pygame.transform.scale(win_text, (scaled_width, scaled_height))
        
        # Позиционируем текст (перемещаем выше, чтобы не было звездочки)
        win_rect = scaled_win_text.get_rect(center=(WIDTH//2, HEIGHT//3 - 30))
        
        # Рисуем более тонкое свечение вокруг текста победы
        glow_surface = pygame.Surface((win_rect.width + 20, win_rect.height + 20), pygame.SRCALPHA)
        for i in range(6, 0, -2):  # Еще меньше слоев свечения
            alpha = 12 - i  # Еще меньше яркость свечения
            pygame.draw.rect(glow_surface, (255, 215, 0, alpha),
                          (10-i, 10-i, win_rect.width + i*2, win_rect.height + i*2), 1)
        
        screen.blit(glow_surface, (win_rect.x - 10, win_rect.y - 10))
        screen.blit(scaled_win_text, win_rect)
        
        # Рисуем информацию о счете
        score_text = self.score_font.render(f"Ваш счет: {score}", True, WHITE)
        message_text = self.message_font.render("Вы достигли конца уровня!", True, (200, 200, 200))
        
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 30))
        message_rect = message_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 70))
        
        screen.blit(score_text, score_rect)
        screen.blit(message_text, message_rect)
        
        # Рисуем минималистичные частицы (очень мало для минимализма)
        for p in self.particles:
            pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), p['size'])
        
        # Обновляем и отрисовываем кнопку
        mouse_pos = pygame.mouse.get_pos()
        self.retry_button.update(mouse_pos)
        self.retry_button.draw(screen)
        
    def handle_click(self, pos):
        return self.retry_button.is_clicked(pos)
