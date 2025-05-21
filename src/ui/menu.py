import pygame
import sys
import os
import math
import random
sys.path.append('.')
from src.constants import *
from src.ui.button import Button

class Menu:
    def __init__(self):
        self.start_button = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 60, "СТАРТ", GREEN)
        self.title_font = pygame.font.Font(None, 80)
        self.subtitle_font = pygame.font.Font(None, 36)
        self.animation_timer = 0
        self.stars = self.create_stars(100)
        self.clouds = self.create_clouds(5)
        
        # Загружаем фон (если есть)
        try:
            bg_path = os.path.join('images', 'backgrownd.jpg')
            self.background = pygame.image.load(bg_path)
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
            self.has_bg = True
        except:
            self.has_bg = False
    
    def create_stars(self, count):
        """Создаем звезды для фона"""
        stars = []
        for _ in range(count):
            stars.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'size': random.randint(1, 3),
                'brightness': random.random(),
                'speed': random.uniform(0.2, 1.0)
            })
        return stars
    
    def create_clouds(self, count):
        """Создаем облака для фона"""
        clouds = []
        for _ in range(count):
            clouds.append({
                'x': random.randint(-100, WIDTH),
                'y': random.randint(50, HEIGHT//3),
                'width': random.randint(100, 250),
                'height': random.randint(30, 80),
                'speed': random.uniform(0.2, 0.5),
                'alpha': random.randint(40, 120)
            })
        return clouds

    def update_stars(self):
        """Обновляем звезды для эффекта мерцания"""
        for star in self.stars:
            star['brightness'] = 0.5 + 0.5 * math.sin(self.animation_timer * star['speed'])
    
    def update_clouds(self):
        """Обновляем положение облаков"""
        for cloud in self.clouds:
            cloud['x'] += cloud['speed']
            if cloud['x'] > WIDTH + 100:
                cloud['x'] = -cloud['width']
                cloud['y'] = random.randint(50, HEIGHT//3)

    def draw(self, screen):
        # Обновляем анимацию
        self.animation_timer += 0.05
        self.update_stars()
        self.update_clouds()
        
        # Рисуем фон
        if self.has_bg:
            # Если есть изображение фона
            screen.blit(self.background, (0, 0))
            # Добавляем полупрозрачный чёрный оверлей для лучшей видимости текста
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
        else:
            # Градиентный фон
            for y in range(HEIGHT):
                color_value = max(0, 50 - y // 10)
                pygame.draw.line(screen, (color_value, color_value, color_value + 30), (0, y), (WIDTH, y))
        
        # Рисуем звезды
        for star in self.stars:
            color = int(255 * star['brightness'])
            pygame.draw.circle(screen, (color, color, color), 
                              (int(star['x']), int(star['y'])), star['size'])
        
        # Рисуем облака
        for cloud in self.clouds:
            cloud_surface = pygame.Surface((cloud['width'], cloud['height']), pygame.SRCALPHA)
            pygame.draw.ellipse(cloud_surface, (255, 255, 255, cloud['alpha']), 
                              (0, 0, cloud['width'], cloud['height']))
            screen.blit(cloud_surface, (int(cloud['x']), int(cloud['y'])))
        
        # Текст заголовка с эффектом свечения
        glow_size = 3 + math.sin(self.animation_timer) * 2
        for offset in range(int(glow_size), 0, -1):
            alpha = 100 - offset * 20
            if alpha > 0:
                glow_color = (255, 215, 0, alpha)  # Золотое свечение
                glow_font = pygame.font.Font(None, 80 + offset * 2)
                glow_text = glow_font.render("ПЛАТФОРМЕР", True, glow_color)
                glow_rect = glow_text.get_rect(center=(WIDTH//2, HEIGHT//3))
                screen.blit(glow_text, glow_rect)
        
        # Основной текст заголовка
        title_text = self.title_font.render("ПЛАТФОРМЕР", True, GOLD)
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//3))
        screen.blit(title_text, title_rect)
        
        # Подзаголовок
        subtitle_text = self.subtitle_font.render("Приключение начинается...", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH//2, HEIGHT//3 + 60))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Обновляем и отрисовываем кнопку
        mouse_pos = pygame.mouse.get_pos()
        self.start_button.update(mouse_pos)
        self.start_button.draw(screen)

    def handle_click(self, pos):
        return self.start_button.is_clicked(pos)
