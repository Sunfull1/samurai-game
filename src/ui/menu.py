import pygame
import sys
sys.path.append('.')
from src.constants import *
from src.ui.button import Button

class Menu:
    def __init__(self):
        self.start_button = Button(WIDTH//2 - 50, HEIGHT//2, 100, 50, "START", GREEN)
        self.title_font = pygame.font.Font(None, 74)

    def draw(self, screen):
        title_text = self.title_font.render("Platform Adventure", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//3))
        screen.blit(title_text, title_rect)
        self.start_button.draw(screen)

    def handle_click(self, pos):
        return self.start_button.is_clicked(pos)
