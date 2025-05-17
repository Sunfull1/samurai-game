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
        
        # Create default image in case textures fail to load
        self.default_image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.default_image.fill((0, 0, 255))  # Blue rectangle as fallback
        
        # Initialize animations dictionary
        self.animations = {
            'right': [],
            'left': [],
            'jump': [],
            'attack_right': [],
            'attack_left': [],
            'dead': []
        }
        
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        try:
            # Load walk animations
            for i in range(1, 9):
                try:
                    img_path = os.path.join(root_dir, 'images', 'player_right', f'player_right{i}.png')
                    if os.path.exists(img_path):
                        print(f"Загрузка ходьбы вправо: {img_path}")
                        img = pygame.image.load(img_path)
                        img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
                        self.animations['right'].append(img)
                    
                    img_path = os.path.join(root_dir, 'images', 'player_left', f'player_left{i}.png')
                    if os.path.exists(img_path):
                        print(f"Загрузка ходьбы влево: {img_path}")
                        img = pygame.image.load(img_path)
                        img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
                        self.animations['left'].append(img)
                except Exception as e:
                    print(f"Ошибка при загрузке анимации ходьбы {i}: {e}")
            
            # Load jump animations
            for i in range(1, 10):
                try:
                    img_path = os.path.join(root_dir, 'images', 'player_jump', 'player_jump', f'Jump{i}.png')
                    if os.path.exists(img_path):
                        print(f"Загрузка прыжка: {img_path}")
                        img = pygame.image.load(img_path)
                        img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
                        self.animations['jump'].append(img)
                except Exception as e:
                    print(f"Ошибка при загрузке анимации прыжка {i}: {e}")
            
            # Load attack animations
            for i in range(1, 5):
                try:
                    img_path = os.path.join(root_dir, 'images', 'player_Attack', 'Attak', f'Attack{i}r.png')
                    if os.path.exists(img_path):
                        print(f"Загрузка атаки: {img_path}")
                        img = pygame.image.load(img_path)
                        img = pygame.transform.scale(img, (PLAYER_WIDTH * 1.5, PLAYER_HEIGHT))
                        self.animations['attack_right'].append(img)
                        # Для левой анимации отразим правую по горизонтали
                        self.animations['attack_left'].append(pygame.transform.flip(img, True, False))
                except Exception as e:
                    print(f"Ошибка при загрузке анимации атаки {i}: {e}")
            
            # Load death animations
            for i in range(1, 7):
                try:
                    img_path = os.path.join(root_dir, 'images', 'player_dead', f'Dead{i}.png')
                    if os.path.exists(img_path):
                        print(f"Загрузка смерти: {img_path}")
                        img = pygame.image.load(img_path)
                        img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
                        self.animations['dead'].append(img)
                except Exception as e:
                    print(f"Ошибка при загрузке анимации смерти {i}: {e}")
            
            # Check if animations were loaded successfully
            for key, frames in self.animations.items():
                if not frames:
                    print(f"Предупреждение: нет кадров для анимации {key}, используем синий прямоугольник")
                    frames.append(self.default_image)
                    
        except Exception as e:
            print(f"Критическая ошибка при загрузке анимаций: {e}")
            # Используем изображение по умолчанию для всех анимаций
            for key in self.animations:
                self.animations[key] = [self.default_image]
        
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
            # Update death animation
            self.death_timer += self.animation_speed
            if self.death_timer >= 1:
                self.death_timer = 0
                if self.death_frame < len(self.animations['dead']) - 1:
                    self.death_frame += 1
            self.current_image = self.animations['dead'][self.death_frame]
            return

        if self.is_attacking:
            # Update attack animation
            self.attack_timer += self.animation_speed * 2  # Speed up attack animation
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
            # Use jump animation with continuous looping
            frame = int(self.animation_timer * 4) % len(self.animations['jump'])
            self.current_image = self.animations['jump'][frame]
            if not self.facing_right:
                self.current_image = pygame.transform.flip(self.current_image, True, False)
            self.animation_timer += self.animation_speed
            if self.animation_timer >= len(self.animations['jump']) / 4:  # Adjust for animation speed
                self.animation_timer = 0
        else:
            # Update walk animation
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
                # Reset to standing frame when not moving
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
