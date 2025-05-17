import pygame
import sys
sys.path.append('.')
from src.constants import *
from src.ui.button import Button

class GameOver:
    def __init__(self):
        self.retry_button = Button(WIDTH//2 - 50, HEIGHT//2, 100, 50, "RETRY", GREEN)
        self.game_over_font = pygame.font.Font(None, 74)
        self.score_font = pygame.font.Font(None, 48)

    def draw(self, screen, score):
        game_over_text = self.game_over_font.render("Game Over!", True, RED)
        score_text = self.score_font.render(f"Final Score: {score}", True, WHITE)
        
        game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//3))
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        self.retry_button.draw(screen)

    def handle_click(self, pos):
        return self.retry_button.is_clicked(pos)
