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
        
        # Параметры для минималистичного и спокойного дизайна
        self.lines = self.create_lines(10)  # Меньше линий для более спокойного вида
        self.soft_spots = self.create_spots(5)  # Меньше пятен
        
        # Загружаем фон (если есть)
        try:
            bg_path = os.path.join('images', 'backgrownd.jpg')
            self.background = pygame.image.load(bg_path)
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
            self.has_bg = True
        except:
            self.has_bg = False
    
    def create_lines(self, count):
        """Создаем спокойные линии для фона"""
        lines = []
        center_x, center_y = WIDTH//2, HEIGHT//3
        for _ in range(count):
            length = random.randint(30, 80)  # Короткие линии
            angle = random.uniform(0, math.pi * 2)
            lines.append({
                'x1': center_x,
                'y1': center_y,
                'x2': center_x + length * math.cos(angle),
                'y2': center_y + length * math.sin(angle),
                'branches': random.randint(0, 1),  # Минимум ответвлений
                'width': 1  # Тонкие линии
            })
        return lines
    
    def create_spots(self, count):
        """Создаем нежные затемненные пятна"""
        spots = []
        for _ in range(count):
            spots.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'radius': random.randint(5, 15),
                'alpha': random.randint(20, 50)  # Очень слабая непрозрачность
            })
        return spots

    def draw(self, screen, score):
        # Обновляем анимацию
        self.animation_timer += 0.03  # Медленнее анимация
        pulse = math.sin(self.animation_timer) * 5  # Менее интенсивная пульсация
        
        # Рисуем спокойный затемненный фон
        if self.has_bg:
            # Если есть изображение фона, делаем его немного темнее и с синим оттенком
            darkened_bg = self.background.copy()
            dark_overlay = pygame.Surface((WIDTH, HEIGHT))
            dark_overlay.fill((0, 0, 40))  # Синий оттенок вместо черного
            dark_overlay.set_alpha(130)  # Еще менее темный
            darkened_bg.blit(dark_overlay, (0, 0))
            screen.blit(darkened_bg, (0, 0))
        else:
            # Спокойный градиентный фон с синим оттенком
            for y in range(HEIGHT):
                blue_value = max(0, min(30, 30 - y // 30))
                pygame.draw.line(screen, (0, 0, blue_value), (0, y), (WIDTH, y))
        
        # Рисуем нежные затемненные пятна
        for spot in self.soft_spots:
            spot_surface = pygame.Surface((spot['radius']*2, spot['radius']*2), pygame.SRCALPHA)
            pygame.draw.circle(spot_surface, (20, 20, 50, spot['alpha']), 
                             (spot['radius'], spot['radius']), spot['radius'])
            screen.blit(spot_surface, (spot['x'] - spot['radius'], spot['y'] - spot['radius']))
        
        # Рисуем спокойные линии
        for line in self.lines:
            pygame.draw.line(screen, (100, 120, 180, 50), 
                           (line['x1'], line['y1']), 
                           (line['x2'], line['y2']), line['width'])
            
            # Добавляем более мягкие ответвления при необходимости
            for i in range(line['branches']):
                branch_length = random.randint(10, 30)  # Короткие ответвления
                branch_angle = random.uniform(0, math.pi)
                mid_x = (line['x1'] + line['x2']) / 2
                mid_y = (line['y1'] + line['y2']) / 2
                end_x = mid_x + branch_length * math.cos(branch_angle)
                end_y = mid_y + branch_length * math.sin(branch_angle)
                pygame.draw.line(screen, (100, 120, 180, 30), 
                               (mid_x, mid_y), (end_x, end_y), line['width'])
        
        # Тень текста (более мягкая)
        shadow_text = self.game_over_font.render("ПОРАЖЕНИЕ", True, (20, 20, 40))
        shadow_rect = shadow_text.get_rect(center=(WIDTH//2 + 2, HEIGHT//3 + 2))
        screen.blit(shadow_text, shadow_rect)
        
        # Основной текст с легкой пульсацией
        game_over_size = 80 + int(pulse/2)  # Уменьшаем пульсацию вдвое
        dynamic_font = pygame.font.Font(None, game_over_size)
        game_over_text = dynamic_font.render("ПОРАЖЕНИЕ", True, (90, 40, 40))  # Более приглушенный красный
        game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//3))
        screen.blit(game_over_text, game_over_rect)
        
        # Отображаем счет с мягкой тенью
        score_shadow = self.score_font.render(f"Ваш счет: {score}", True, (40, 40, 60))
        score_text = self.score_font.render(f"Ваш счет: {score}", True, (200, 200, 220))
        
        score_shadow_rect = score_shadow.get_rect(center=(WIDTH//2 + 1, HEIGHT//2 - 48))
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        
        screen.blit(score_shadow, score_shadow_rect)
        screen.blit(score_text, score_rect)
        
        # Дополнительное сообщение без мерцания
        message_text = self.message_font.render("Игра завершена", True, (200, 200, 220))
        message_rect = message_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(message_text, message_rect)
        
        # Обновляем и отрисовываем кнопку
        mouse_pos = pygame.mouse.get_pos()
        self.retry_button.update(mouse_pos)
        self.retry_button.draw(screen)

    def handle_click(self, pos):
        return self.retry_button.is_clicked(pos)
