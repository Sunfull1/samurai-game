import pygame
import sys
import os
import math
import random
sys.path.append('.')
from src.constants import *
from src.ui.button import Button

class GameOver:
    def __init__(self):
        self.retry_button = Button(WIDTH//2 - 125, HEIGHT//2 + 50, 250, 60, "НАЧАТЬ ЗАНОВО", (70, 100, 160))  # Спокойный синий цвет
        self.game_over_font = pygame.font.Font(None, 80)
        self.score_font = pygame.font.Font(None, 48)
        self.message_font = pygame.font.Font(None, 36)
        self.animation_timer = 0
        
        # Параметры для анимации эффекта сломанного экрана
        self.cracks = self.create_cracks(20)
        self.blood_splats = self.create_blood_splats(15)
        
        # Загружаем фон (если есть)
        try:
            bg_path = os.path.join('images', 'backgrownd.jpg')
            self.background = pygame.image.load(bg_path)
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
            self.has_bg = True
        except:
            self.has_bg = False
            
    def create_cracks(self, count):
        """Создаем более спокойные линии вместо трещин"""
        cracks = []
        center_x, center_y = WIDTH//2, HEIGHT//3
        for _ in range(count//2):  # Меньше линий для более спокойного вида
            length = random.randint(30, 100)  # Короче линии
            angle = random.uniform(0, math.pi * 2)
            cracks.append({
                'x1': center_x,
                'y1': center_y,
                'x2': center_x + length * math.cos(angle),
                'y2': center_y + length * math.sin(angle),
                'branches': random.randint(0, 1),  # Меньше ответвлений
                'width': 1  # Тонкие линии
            })
        return cracks
    
    def create_blood_splats(self, count):
        """Создаем затемненные пятна вместо крови для спокойного вида"""
        splats = []
        for _ in range(count//3):  # Меньше пятен
            splats.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'radius': random.randint(5, 20),
                'alpha': random.randint(30, 70)  # Гораздо менее интенсивные
            })
        return splats
        
    def draw(self, screen, score):
        # Обновляем анимацию
        self.animation_timer += 0.05
        pulse = math.sin(self.animation_timer) * 10
        
        # Рисуем спокойный затемненный фон
        if self.has_bg:
            # Если есть изображение фона, делаем его немного темнее и с синим оттенком
            darkened_bg = self.background.copy()
            dark_overlay = pygame.Surface((WIDTH, HEIGHT))
            dark_overlay.fill((0, 0, 40))  # Синий оттенок вместо черного
            dark_overlay.set_alpha(150)  # Менее темный
            darkened_bg.blit(dark_overlay, (0, 0))
            screen.blit(darkened_bg, (0, 0))
        else:
            # Спокойный градиентный фон с синим оттенком
            for y in range(HEIGHT):
                blue_value = max(0, min(30, 30 - y // 30))
                pygame.draw.line(screen, (0, 0, blue_value), (0, y), (WIDTH, y))
        
        # Рисуем нежные затемненные пятна вместо крови
        for splat in self.blood_splats:
            splat_surface = pygame.Surface((splat['radius']*2, splat['radius']*2), pygame.SRCALPHA)
            pygame.draw.circle(splat_surface, (20, 20, 50, splat['alpha']), 
                             (splat['radius'], splat['radius']), splat['radius'])
            screen.blit(splat_surface, (splat['x'] - splat['radius'], splat['y'] - splat['radius']))
        
        # Рисуем спокойные линии вместо трещин
        for crack in self.cracks:
            pygame.draw.line(screen, (100, 120, 180), 
                           (crack['x1'], crack['y1']), 
                           (crack['x2'], crack['y2']), crack['width'])
            
            # Добавляем более мягкие ответвления 
            for i in range(crack['branches']):
                branch_length = random.randint(10, 40)  # Короче ответвления
                branch_angle = random.uniform(0, math.pi)
                mid_x = (crack['x1'] + crack['x2']) / 2
                mid_y = (crack['y1'] + crack['y2']) / 2
                end_x = mid_x + branch_length * math.cos(branch_angle)
                end_y = mid_y + branch_length * math.sin(branch_angle)
                pygame.draw.line(screen, (100, 120, 180), 
                               (mid_x, mid_y), (end_x, end_y), crack['width'])
        
        # Текст Game Over без эффекта дрожания
        shake_x = 0  # Убираем дрожание
        shake_y = 0  # Убираем дрожание
        
        # Тень текста (более мягкая)
        shadow_text = self.game_over_font.render("ПОРАЖЕНИЕ", True, (20, 20, 40))
        shadow_rect = shadow_text.get_rect(center=(WIDTH//2 + 2, HEIGHT//3 + 2))
        screen.blit(shadow_text, shadow_rect)
        
        # Основной текст с легкой пульсацией
        game_over_size = 80 + int(pulse/2)  # Уменьшаем пульсацию вдвое
        dynamic_font = pygame.font.Font(None, game_over_size)
        game_over_text = dynamic_font.render("ПОРАЖЕНИЕ", True, (100, 40, 40))  # Менее яркий красный
        game_over_rect = game_over_text.get_rect(center=(WIDTH//2 + shake_x, HEIGHT//3 + shake_y))
        screen.blit(game_over_text, game_over_rect)
        
        # Отображаем счет с мягкой тенью
        score_shadow = self.score_font.render(f"Ваш счет: {score}", True, (40, 40, 60))
        score_text = self.score_font.render(f"Ваш счет: {score}", True, (220, 220, 240))
        
        score_shadow_rect = score_shadow.get_rect(center=(WIDTH//2 + 1, HEIGHT//2 - 48))
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        
        screen.blit(score_shadow, score_shadow_rect)
        screen.blit(score_text, score_rect)
        
        # Дополнительное сообщение без мерцания
        alpha = 200  # Постоянная прозрачность для спокойствия
        message_surface = pygame.Surface((400, 40), pygame.SRCALPHA)
        message_text = self.message_font.render("Игра завершена", True, (200, 200, 220, alpha))
        message_rect = message_text.get_rect(center=(200, 20))
        message_surface.blit(message_text, message_rect)
        screen.blit(message_surface, (WIDTH//2 - 200, HEIGHT//2))
        
        # Обновляем и отрисовываем кнопку
        mouse_pos = pygame.mouse.get_pos()
        self.retry_button.update(mouse_pos)
        self.retry_button.draw(screen)

    def handle_click(self, pos):
        return self.retry_button.is_clicked(pos)
