import pygame
import sys
sys.path.append('.')
from src.constants import *

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = self.lighten_color(color, 30)
        self.font = pygame.font.Font(None, 36)
        self.is_hovered = False
        self.pulse_effect = 0
        self.pulse_direction = 1
        self.pulse_speed = 0.1
        self.pulse_max = 5
        
    def lighten_color(self, color, amount):
        r = min(255, color[0] + amount)
        g = min(255, color[1] + amount)
        b = min(255, color[2] + amount)
        return (r, g, b)

    def draw(self, screen):
        # Обновляем эффект пульсации
        self.pulse_effect += self.pulse_speed * self.pulse_direction
        if self.pulse_effect >= self.pulse_max or self.pulse_effect <= 0:
            self.pulse_direction *= -1
        
        # Определяем цвет на основе наведения мыши
        current_color = self.hover_color if self.is_hovered else self.color
        
        # Создаем прямоугольник с тенью
        shadow_rect = pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.rect.width, self.rect.height)
        pygame.draw.rect(screen, (50, 50, 50, 150), shadow_rect, border_radius=8)
        
        # Основной прямоугольник с закругленными углами
        pygame.draw.rect(screen, current_color, self.rect, border_radius=8)
        
        # Блики по краям (эффект стекла)
        highlight_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, 5)
        pygame.draw.rect(screen, self.lighten_color(current_color, 50), highlight_rect, border_radius=4)
        
        # Увеличиваем размер шрифта, если кнопка активна
        font_size = 36 + (self.pulse_effect if self.is_hovered else 0)
        button_font = pygame.font.Font(None, int(font_size))
        
        # Текст с тенью
        text_shadow = button_font.render(self.text, True, (30, 30, 30))
        text_main = button_font.render(self.text, True, WHITE)
        
        shadow_rect = text_shadow.get_rect(center=(self.rect.center[0] + 2, self.rect.center[1] + 2))
        text_rect = text_main.get_rect(center=self.rect.center)
        
        screen.blit(text_shadow, shadow_rect)
        screen.blit(text_main, text_rect)

    def update(self, mouse_pos):
        prev_hover = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Если состояние наведения изменилось, сбрасываем эффект пульсации
        if prev_hover != self.is_hovered:
            self.pulse_effect = 0
            self.pulse_direction = 1
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
