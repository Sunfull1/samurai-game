import pygame
import sys
import os

# Helper function to get correct resource path
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Not running in a PyInstaller bundle
        # For player.py, the images folder is two levels up from src/player/
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    return os.path.join(base_path, relative_path)

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
                path = resource_path(os.path.join('images', 'player_run', 'player_right', f'player_right{i}.png'))
                # if os.path.exists(path): # This check is less reliable with _MEIPASS
                image = pygame.image.load(path)
                image = pygame.transform.scale(image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                animations['right'].append(image)
            except Exception as e:
                print(f"Ошибка загрузки {path}: {e}")
        
        # Загрузка анимаций ходьбы влево
        for i in range(1, 9):
            try:
                path = resource_path(os.path.join('images', 'player_run', 'player_left', f'player_left{i}.png'))
                # if os.path.exists(path):
                image = pygame.image.load(path)
                image = pygame.transform.scale(image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                animations['left'].append(image)
            except Exception as e:
                print(f"Ошибка загрузки {path}: {e}")
        
        # Загрузка анимаций прыжка вправо
        for i in range(1, 5):
            try:
                path = resource_path(os.path.join('images', 'player_jump', 'jumpr', f'Jump{i}r.png'))
                # if os.path.exists(path):
                image = pygame.image.load(path)
                image = pygame.transform.scale(image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                animations['jump_right'].append(image)
            except Exception as e:
                print(f"Ошибка загрузки {path}: {e}")
          # Загрузка анимаций прыжка влево
        for i in range(1, 5):
            try:
                path = resource_path(os.path.join('images', 'player_jump', 'jumpl', f'Jump{i}l.png'))
                # if os.path.exists(path):
                image = pygame.image.load(path)
                image = pygame.transform.scale(image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                animations['jump_left'].append(image)
            except Exception as e:
                print(f"Ошибка загрузки {path}: {e}")
        
        # Загрузка анимаций атаки
        attack_files = [
            'Attack1r.png',
            'Attack2.png',
            'Attack3.png',
            'Attack4.png'
        ]
        for i, filename in enumerate(attack_files):
            try:
                path = resource_path(os.path.join('images', 'player_Attack', 'Attak', filename))
                # if os.path.exists(path):
                # Загружаем исходное изображение
                original_image = pygame.image.load(path)
                
                # Определяем размеры, сохраняя пропорции
                orig_width, orig_height = original_image.get_size()
                scale_factor = PLAYER_HEIGHT / orig_height  # Масштабируем по высоте персонажа
                attack_width = int(orig_width * scale_factor)
                attack_height = PLAYER_HEIGHT
                
                # Масштабируем с сохранением пропорций
                image = pygame.transform.scale(original_image, (attack_width, attack_height))
                animations['attack_right'].append(image)
                
                # Зеркально отображаем для атаки влево
                flipped_image = pygame.transform.flip(image, True, False)
                animations['attack_left'].append(flipped_image)
                print(f"Успешно загружена анимация атаки: {filename} (размер: {attack_width}x{attack_height})")
            except Exception as e:
                print(f"Ошибка загрузки анимации атаки {filename}: {e}")
        
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
            
            # Если игрок атакует, показываем анимацию атаки
            if self.is_attacking:
                # Анимация атаки имеет приоритет над другими анимациями
                attack_key = 'attack_right' if self.facing_right else 'attack_left'
                if self.animations[attack_key]:
                    attack_frames = len(self.animations[attack_key])
                    # Увеличиваем счетчик кадров
                    self.current_frame = (self.current_frame + 1) % attack_frames
                    self.current_image = self.animations[attack_key][self.current_frame]
                    
                    # Если достигли последнего кадра, заканчиваем атаку
                    if self.current_frame == attack_frames - 1:
                        self.is_attacking = False
                        self.current_frame = 0
            elif self.jumping:
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
            else:                # Анимация покоя (первый кадр анимации бега)
                animation_key = 'right' if self.facing_right else 'left'                
                if self.animations[animation_key]:
                    self.current_image = self.animations[animation_key][0]
    
    def draw(self, screen, camera):
        # Рисуем игрока с учетом камеры
        screen_x = self.x - camera.camera.x
        screen_y = self.y
        
        # При атаке учитываем возможное изменение размеров анимации
        if self.is_attacking:
            # Центрируем изображение атаки по горизонтали относительно позиции игрока
            image_width = self.current_image.get_width()
            
            # Регулировка позиции в зависимости от направления атаки
            if self.facing_right:
                attack_x = screen_x  # Атака вправо от текущей позиции
            else:
                attack_x = screen_x - (image_width - self.width)  # Атака влево
            
            # Отрисовка анимации атаки
            screen.blit(self.current_image, (attack_x, screen_y))
            
            # Для отладки можно нарисовать рамку
            # pygame.draw.rect(screen, RED, (screen_x, screen_y, self.width, self.height), 1)
        else:
            # Обычная отрисовка
            screen.blit(self.current_image, (screen_x, screen_y))
        
        # Отображаем счет
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))
    
    def start_attack(self):
        # Начинаем атаку только если сейчас не атакуем
        if not self.is_attacking:
            self.is_attacking = True
            self.current_frame = 0  # Сбрасываем счетчик кадров для анимации атаки
            print("Игрок начал атаку!")
