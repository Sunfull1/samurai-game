import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player properties
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.vel_x = 0
        self.vel_y = 0
        self.jumping = False
        self.on_ground = False
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8

    def move(self):
        # Apply gravity
        self.vel_y += self.gravity
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Keep player in bounds
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.vel_y = 0
            self.on_ground = True
            self.jumping = False

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

# Platform class
class Platform:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.height = 20

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = 2
        self.direction = 1  # 1 for right, -1 for left

    def move(self, player):
        # Move towards player
        if self.x < player.x:
            self.x += self.speed
        else:
            self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

# Create game objects
player = Player(WIDTH // 2, HEIGHT - 60)
platforms = [
    Platform(100, HEIGHT - 100, 200),
    Platform(400, HEIGHT - 200, 200),
    Platform(700, HEIGHT - 300, 200),
    Platform(200, HEIGHT - 400, 200)
]
enemies = [
    Enemy(100, HEIGHT - 150),
    Enemy(600, HEIGHT - 350)
]

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not player.jumping:
                player.vel_y = player.jump_power
                player.jumping = True
                player.on_ground = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    player.vel_x = 0
    if keys[pygame.K_LEFT]:
        player.vel_x = -player.speed
    if keys[pygame.K_RIGHT]:
        player.vel_x = player.speed

    # Update game objects
    player.move()
    
    # Platform collision
    for platform in platforms:
        if (player.y + player.height >= platform.y and 
            player.y < platform.y and 
            player.x + player.width > platform.x and 
            player.x < platform.x + platform.width):
            if player.vel_y >= 0:
                player.y = platform.y - player.height
                player.vel_y = 0
                player.on_ground = True
                player.jumping = False

    # Update enemies
    for enemy in enemies:
        enemy.move(player)

    # Check for collision with enemies
    for enemy in enemies:
        if (player.x < enemy.x + enemy.width and
            player.x + player.width > enemy.x and
            player.y < enemy.y + enemy.height and
            player.y + player.height > enemy.y):
            print("Game Over!")
            running = False

    # Draw everything
    screen.fill(BLACK)
    player.draw(screen)
    for platform in platforms:
        platform.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()