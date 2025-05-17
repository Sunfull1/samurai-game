import pygame
import sys
import os

# Add the game root directory to Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from src.constants import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.vel_x = 0
        self.vel_y = 0
        self.jumping = False
        self.on_ground = False
        self.speed = PLAYER_SPEED
        self.jump_power = PLAYER_JUMP_POWER
        self.gravity = PLAYER_GRAVITY
        self.score = 0
        self.facing_right = True
        self.is_dead = False
        self.is_attacking = False
        
        # Animation properties
        self.animation_frame = 0
        self.animation_speed = ANIMATION_SPEED
        self.animation_timer = 0
        self.attack_frame = 0
        self.attack_timer = 0
        self.death_frame = 0
        self.death_timer = 0
          
        # Load animations
        self.animations = {
            'right': [],
            'left': [],
            'jump': [],  # Единая анимация прыжка
            'attack_right': [],
            'attack_left': [],
            'dead': []
        }
        
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
          # Load walk animations
        print("Загрузка анимаций ходьбы...")
        for i in range(1, 9):
            try:
                # Load right animation
                img_path = os.path.join(root_dir, 'images', 'player_right', f'player_right{i}.png')
                if os.path.exists(img_path):
                    img = pygame.image.load(img_path)
                    img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
                    self.animations['right'].append(img)
                else:
                    print(f"Файл не найден: {img_path}")
                    self.animations['right'].append(self.default_image)

                # Load left animation
                img_path = os.path.join(root_dir, 'images', 'player_left', f'player_left{i}.png')
                if os.path.exists(img_path):
                    img = pygame.image.load(img_path)
                    img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
                    self.animations['left'].append(img)
                else:
                    print(f"Файл не найден: {img_path}")
                    self.animations['left'].append(pygame.transform.flip(self.default_image, True, False))
            except Exception as e:
                print(f"Ошибка при загрузке анимации ходьбы {i}: {e}")
                self.animations['right'].append(self.default_image)
                self.animations['left'].append(pygame.transform.flip(self.default_image, True, False))
              
        # Загрузка анимации прыжка
        print("Начинаю загрузку анимации прыжка...")
        jump_frames_loaded = 0
        for i in range(1, 10):
            img_path = os.path.join(root_dir, 'images', 'player_jump', 'player_jump', f'Jump{i}.png')
            try:
                img = pygame.image.load(img_path)
                img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
                self.animations['jump'].append(img)
                jump_frames_loaded += 1
            except Exception as e:
                print(f"Ошибка при загрузке кадра прыжка {i}: {e}")
                print(f"Путь к файлу: {img_path}")
        
        print(f"Загружено {jump_frames_loaded} из 9 кадров прыжка")
          # Load attack animations
        print("Загрузка анимаций атаки...")
        for i in range(1, 5):
            try:
                img_path = os.path.join(root_dir, 'images', 'player_Attack', 'Attak', f'Attack{i}.png')
                if os.path.exists(img_path):
                    img = pygame.image.load(img_path)
                    img = pygame.transform.scale(img, (PLAYER_WIDTH * 1.5, PLAYER_HEIGHT))
                    self.animations['attack_right'].append(img)
                else:
                    print(f"Файл не найден: {img_path}")
                    # Create a default attack frame
                    img = pygame.Surface((int(PLAYER_WIDTH * 1.5), PLAYER_HEIGHT))
                    img.fill((255, 0, 0))  # Red rectangle for attack
                    self.animations['attack_right'].append(img)
            except Exception as e:
                print(f"Ошибка при загрузке кадра атаки {i}: {e}")
                # Create a default attack frame
                img = pygame.Surface((int(PLAYER_WIDTH * 1.5), PLAYER_HEIGHT))
                img.fill((255, 0, 0))  # Red rectangle for attack
                self.animations['attack_right'].append(img)
            # Create left attack animation by flipping the right animation
            flipped_img = pygame.transform.flip(img, True, False)
            self.animations['attack_left'].append(flipped_img)
              # Load death animations
        print("Загрузка анимаций смерти...")
        for i in range(1, 7):
            try:
                img_path = os.path.join(root_dir, 'images', 'player_dead', f'Dead{i}.png')
                if os.path.exists(img_path):
                    img = pygame.image.load(img_path)
                    img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
                    self.animations['dead'].append(img)
                else:
                    print(f"Файл не найден: {img_path}")
                    self.animations['dead'].append(self.default_image)
            except Exception as e:
                print(f"Ошибка при загрузке кадра смерти {i}: {e}")
                self.animations['dead'].append(self.default_image)
            
        # Current image
        self.current_image = self.animations['right'][0]
    
    def move(self):
        # Apply gravity
        self.vel_y += self.gravity
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Keep player in bounds
        if self.x < 0:
            self.x = 0
        if self.x > LEVEL_WIDTH - self.width:
            self.x = LEVEL_WIDTH - self.width
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.vel_y = 0
            self.on_ground = True
            self.jumping = False
    
    def update_animation(self):
        if self.is_dead:
            # Обновление анимации смерти
            self.death_timer += self.animation_speed
            if self.death_timer >= 1:
                self.death_timer = 0
                if self.death_frame < len(self.animations['dead']) - 1:
                    self.death_frame += 1
            self.current_image = self.animations['dead'][self.death_frame]
            return

        if self.is_attacking:
            # Обновление анимации атаки
            self.attack_timer += self.animation_speed * 2  # Ускоренная анимация атаки
            if self.attack_timer >= 1:
                self.attack_timer = 0
                self.attack_frame += 1
                if self.attack_frame >= len(self.animations['attack_right']):
                    self.attack_frame = 0
                    self.is_attacking = False
            
            if self.facing_right:
                self.current_image = self.animations['attack_right'][min(self.attack_frame, len(self.animations['attack_right'])-1)]
            else:
                self.current_image = self.animations['attack_left'][min(self.attack_frame, len(self.animations['attack_left'])-1)]
            return

        if self.jumping:
            # Обновленная логика анимации прыжка
            if self.vel_y < 0:  # Подъем
                # Используем первые 4 кадра для подъема (0-3)
                progress = abs(self.vel_y) / abs(self.jump_power)
                frame = min(3, int(progress * 4))
            else:  # Падение
                # Используем оставшиеся 5 кадров для падения (4-8)
                progress = min(1.0, self.vel_y / (self.jump_power * -2))
                frame = min(8, 4 + int(progress * 5))
            
            # Проверяем, что индекс кадра действителен
            frame = max(0, min(frame, len(self.animations['jump']) - 1))
            
            # Получаем текущий кадр анимации прыжка
            jump_image = self.animations['jump'][frame]
            # Отражаем изображение, если персонаж смотрит влево
            if not self.facing_right:
                self.current_image = pygame.transform.flip(jump_image, True, False)
            else:
                self.current_image = jump_image
        else:
            # Обновление анимации ходьбы
            if abs(self.vel_x) > 0:
                self.animation_timer += self.animation_speed
                if self.animation_timer >= 1:
                    self.animation_timer = 0
                    self.animation_frame = (self.animation_frame + 1) % len(self.animations['right'])
                    
                if self.facing_right:
                    self.current_image = self.animations['right'][self.animation_frame]
                else:
                    self.current_image = self.animations['left'][self.animation_frame]
            else:
                # Сброс на стоячий кадр при отсутствии движения
                self.animation_frame = 0
                if self.facing_right:
                    self.current_image = self.animations['right'][0]
                else:
                    self.current_image = self.animations['left'][0]
    
    def start_attack(self):
        if not self.is_attacking and not self.is_dead:
            self.is_attacking = True
            self.attack_frame = 0
            self.attack_timer = 0
    
    def start_death(self):
        if not self.is_dead:
            self.is_dead = True
            self.death_frame = 0
            self.death_timer = 0
    
    def draw(self, screen, camera):
        # Update animation
        self.update_animation()
        
        # Calculate draw position
        player_rect = camera.apply(self)
        
        # Draw player sprite with attack offset
        if self.is_attacking:
            # When attacking, the sprite is wider, so adjust x position
            if self.facing_right:
                screen.blit(self.current_image, (player_rect.x - (PLAYER_WIDTH * 0.25), player_rect.y))
            else:
                screen.blit(self.current_image, player_rect)
        else:
            screen.blit(self.current_image, player_rect)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))
