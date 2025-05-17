import pygame
import random
import math
import sys
import os

# Add the game root directory to Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from src.constants import *

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.speed = ENEMY_SPEED
        self.direction = 1  # 1 for right, -1 for left
        self.alive = True
        self.initial_x = x
        self.initial_y = y
        self.patrol_range = ENEMY_PATROL_RANGE
        
        # Load enemy texture
        try:
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            img_path = os.path.join(root_dir, 'images', 'enemies', 'robot_flor.png')
            self.texture = pygame.image.load(img_path)
            self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
        except:
            self.texture = None

    def move(self, player):
        if not self.alive:
            return
            
        # Simple patrol behavior
        self.x += self.speed * self.direction
        
        # Change direction if reached patrol limit
        if self.x > self.initial_x + self.patrol_range:
            self.x = self.initial_x + self.patrol_range
            self.direction = -1
        elif self.x < self.initial_x - self.patrol_range:
            self.x = self.initial_x - self.patrol_range
            self.direction = 1

    def draw(self, screen, camera):
        if not self.alive:
            return
            
        enemy_rect = camera.apply(self)
        if hasattr(self, 'texture') and self.texture:
            # Flip the texture based on direction
            if self.direction < 0:
                flipped_texture = pygame.transform.flip(self.texture, True, False)
                screen.blit(flipped_texture, enemy_rect)
            else:
                screen.blit(self.texture, enemy_rect)
        else:
            # Fallback to rectangle if texture not available
            pygame.draw.rect(screen, RED, enemy_rect)
