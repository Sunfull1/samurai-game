import pygame
import sys
import os

# Add the game root directory to Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from src.constants import *

class Player:
    def __init__(self, x, y):
        # Позиция и размеры
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        
        # Физика
        self.vel_x = 0
        self.vel_y = 0
        self.speed = PLAYER_SPEED
        self.jump_power = PLAYER_JUMP_POWER
        self.gravity = PLAYER_GRAVITY
        
        # Состояния
        self.on_ground = True
        self.jumping = False
        self.facing_right = True
        self.is_attacking = False
        self.score = 0
        
        # Анимация
        self.current_frame = 0
        self.animation_timer = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 1000 // ANIMATION_FRAME_SPEED  # Конвертируем кадры в секунду в миллисекунды
        self.animations = self._load_animations()
        self.current_image = self.animations['right'][0] if self.animations['right'] else pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
    
    def _load_animations(self):
        animations = {
            'right': [],
            'left': [],
            'jump_right': [],
            'jump_left': [],
            'attack_right': [],
            'attack_left': [],
        }
        
        # Загрузка анимаций ходьбы вправо
        for i in range(1, 9):
            try:
                path = os.path.join('images', 'player_run', 'player_right', f'player_right{i}.png')
                if os.path.exists(path):
                    image = pygame.image.load(path)
                    image = pygame.transform.scale(image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                    animations['right'].append(image)
            except Exception as e:
                print(f"Ошибка загрузки {path}: {e}")
        
        # Загрузка анимаций ходьбы влево
        for i in range(1, 9):
            try:
                path = os.path.join('images', 'player_run', 'player_left', f'player_left{i}.png')
                if os.path.exists(path):
                    image = pygame.image.load(path)
                    image = pygame.transform.scale(image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                    animations['left'].append(image)
            except Exception as e:
                print(f"Ошибка загрузки {path}: {e}")
        
        # Загрузка анимаций прыжка вправо
        for i in range(1, 5):
            try:
                path = os.path.join('images', 'player_jump', 'jumpr', f'Jump{i}r.png')
                if os.path.exists(path):
                    image = pygame.image.load(path)
                    image = pygame.transform.scale(image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                    animations['jump_right'].append(image)
            except Exception as e:
                print(f"Ошибка загрузки {path}: {e}")
        
        # Загрузка анимаций прыжка влево
        for i in range(1, 5):
            try:
                path = os.path.join('images', 'player_jump', 'jumpl', f'Jump{i}l.png')
                if os.path.exists(path):
                    image = pygame.image.load(path)
                    image = pygame.transform.scale(image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                    animations['jump_left'].append(image)
            except Exception as e:
                print(f"Ошибка загрузки {path}: {e}")
        
        # Создаем изображения по умолчанию
        for key in animations:
            if not animations[key]:
                default_image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
                default_image.fill(BLUE)
                animations[key] = [default_image]
        
        return animations
    
    def move(self):
        # Применяем гравитацию
        self.vel_y += self.gravity
        
        # Обновляем позицию
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Ограничиваем движение по X
        if self.x < 0:
            self.x = 0
        if self.x > LEVEL_WIDTH - self.width:
            self.x = LEVEL_WIDTH - self.width
        
        # Обновляем анимацию
        self.update_animation()
    
    def update_animation(self):
        current_time = pygame.time.get_ticks()
        
        # Проверяем, прошло ли достаточно времени для смены кадра
        if current_time - self.last_update >= self.frame_delay:
            self.last_update = current_time
            
            if self.jumping:
                # Анимация прыжка
                jump_key = 'jump_right' if self.facing_right else 'jump_left'
                if self.animations[jump_key]:
                    frame = 1 if self.vel_y < 0 else 2
                    self.current_image = self.animations[jump_key][min(frame, len(self.animations[jump_key]) - 1)]
            elif self.vel_x != 0:
                # Анимация бега
                animation_key = 'right' if self.facing_right else 'left'
                if self.animations[animation_key]:
                    self.current_frame = (self.current_frame + 1) % len(self.animations[animation_key])
                    self.current_image = self.animations[animation_key][self.current_frame]
            else:
                # Анимация покоя (первый кадр анимации бега)
                animation_key = 'right' if self.facing_right else 'left'
                if self.animations[animation_key]:
                    self.current_image = self.animations[animation_key][0]
    
    def draw(self, screen, camera):
        # Рисуем игрока с учетом камеры
        screen_x = self.x - camera.camera.x
        screen_y = self.y
        screen.blit(self.current_image, (screen_x, screen_y))
        
        # Отображаем счет
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))
    
    def start_attack(self):
        self.is_attacking = True
