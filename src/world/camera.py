import pygame
import sys
import os

# Add the game root directory to Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from src.constants import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return pygame.Rect(entity.x - self.camera.x, entity.y, entity.width, entity.height)

    def update(self, target):
        x = -target.x + WIDTH // 2
        x = min(0, x)  # stop scrolling at the left edge
        x = max(-(LEVEL_WIDTH - WIDTH), x)  # stop scrolling at the right edge
        self.camera.x = -x
