import pygame
import sys
import os

# Add the game root directory to Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from src.constants import *

class Player:
    def __init__(self, x, y):
        # ...existing code...
        
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
                        print(f"Загрузка прыжка {i}: {img_path}")
                        img = pygame.image.load(img_path)
                        img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
                        self.animations['jump'].append(img)
                    else:
                        print(f"Файл не найден: {img_path}")
                except Exception as e:
                    print(f"Ошибка при загрузке анимации прыжка {i}: {e}")
            
            # Load attack animations
            for i in range(1, 5):
                try:
                    img_path = os.path.join(root_dir, 'images', 'player_Attack', 'Attak', f'Attack{i}.png')
                    if os.path.exists(img_path):
                        print(f"Загрузка атаки {i}: {img_path}")
                        img = pygame.image.load(img_path)
                        img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))  # Теперь без увеличения размера
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
                        print(f"Загрузка смерти {i}: {img_path}")
                        img = pygame.image.load(img_path)
                        img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
                        self.animations['dead'].append(img)
                except Exception as e:
                    print(f"Ошибка при загрузке анимации смерти {i}: {e}")
        except Exception as e:
            print(f"Критическая ошибка при загрузке анимаций: {e}")
            for key in self.animations:
                self.animations[key] = [self.default_image]
        
        self.current_image = self.animations['right'][0]
    
    def draw(self, screen, camera):
        # Update animation
        self.update_animation()
        
        # Calculate draw position
        player_rect = camera.apply(self)
        
        # Draw player sprite without offset for attack
        screen.blit(self.current_image, player_rect)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))
