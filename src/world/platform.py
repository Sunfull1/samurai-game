import pygame
import sys
import os

# Add the game root directory to Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from src.constants import *

class Platform:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.height = PLATFORM_HEIGHT
        self.texture = None

    def set_texture(self, texture):
        self.texture = pygame.transform.scale(texture, (self.width, self.height))

    def draw(self, screen, camera):
        platform_rect = camera.apply(self)
        if self.texture:
            screen.blit(self.texture, platform_rect)
        else:
            pygame.draw.rect(screen, GREEN, platform_rect)
