import pygame

# Display settings
WIDTH = 800
HEIGHT = 600
LEVEL_WIDTH = 3200  # 4 screens wide
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)  # Золотой цвет для сообщения о победе

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
DYING = 3
WIN = 4  # Новое состояние для победы

# Player settings
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 80
PLAYER_SPEED = 5
PLAYER_JUMP_POWER = -15
PLAYER_GRAVITY = 0.8
ATTACK_RANGE = 80
ANIMATION_FRAME_SPEED = 8  # Кадров в секунду для анимации бега

# Platform settings
PLATFORM_WIDTH = 100  # Уменьшаем ширину платформы
PLATFORM_HEIGHT = 40  # Оптимальная высота для платформы

# Enemy settings
ENEMY_WIDTH = 60
ENEMY_HEIGHT = 60
ENEMY_SPEED = 2
ENEMY_PATROL_RANGE = 150

# Animation settings
ANIMATION_SPEED = 0.2
ATTACK_ANIMATION_SPEED = 0.15
DEATH_ANIMATION_SPEED = 0.1
ATTACK_RANGE = 80
