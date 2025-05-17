import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
LEVEL_WIDTH = 3200  # 4 screens wide
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario-style Platformer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Camera class
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

# Player class
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
        self.score = 0
        self.facing_right = True
    
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
    
    def draw(self, screen, camera):
        player_rect = camera.apply(self)
        pygame.draw.rect(screen, BLUE, player_rect)
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))

# Platform class
class Platform:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.height = 20

    def draw(self, screen, camera):
        platform_rect = camera.apply(self)
        pygame.draw.rect(screen, GREEN, platform_rect)

# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = 2
        self.direction = 1  # 1 for right, -1 for left
        self.alive = True
        self.initial_x = x
        self.patrol_range = 100

    def move(self, player):
        if not self.alive:
            return
            
        # Patrol back and forth
        if abs(self.x - self.initial_x) > self.patrol_range:
            self.direction *= -1
        self.x += self.speed * self.direction

    def draw(self, screen, camera):
        if not self.alive:
            return
        enemy_rect = camera.apply(self)
        pygame.draw.rect(screen, RED, enemy_rect)

# Create game objects
player = Player(50, HEIGHT - 100)
camera = Camera(WIDTH, HEIGHT)

# Create a longer level with more platforms and enemies
platforms = [
    # Ground platforms
    Platform(0, HEIGHT - 40, 800),
    Platform(900, HEIGHT - 40, 800),
    Platform(1800, HEIGHT - 40, 800),
    Platform(2700, HEIGHT - 40, 500),
    
    # Floating platforms
    Platform(300, HEIGHT - 150, 200),
    Platform(600, HEIGHT - 250, 200),
    Platform(900, HEIGHT - 200, 200),
    Platform(1200, HEIGHT - 300, 200),
    Platform(1500, HEIGHT - 250, 200),
    Platform(1800, HEIGHT - 350, 200),
    Platform(2100, HEIGHT - 200, 200),
    Platform(2400, HEIGHT - 300, 200),
    Platform(2700, HEIGHT - 250, 200),
]

enemies = [
    Enemy(400, HEIGHT - 80),
    Enemy(800, HEIGHT - 190),
    Enemy(1200, HEIGHT - 80),
    Enemy(1600, HEIGHT - 290),
    Enemy(2000, HEIGHT - 80),
    Enemy(2400, HEIGHT - 340),
    Enemy(2800, HEIGHT - 290),
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
        player.facing_right = False
    if keys[pygame.K_RIGHT]:
        player.vel_x = player.speed
        player.facing_right = True

    # Update game objects
    player.move()
    
    # Platform collision
    player.on_ground = False
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
        if not enemy.alive:
            continue
            
        # Check if player is jumping on top of the enemy
        if (player.x + player.width > enemy.x and 
            player.x < enemy.x + enemy.width and
            player.y + player.height > enemy.y and
            player.y + player.height < enemy.y + enemy.height and
            player.vel_y > 0):
            # Kill enemy and bounce player
            enemy.alive = False
            player.vel_y = player.jump_power
            player.score += 100
        # Check if player collides with enemy from the side
        elif (player.x < enemy.x + enemy.width and
             player.x + player.width > enemy.x and
             player.y < enemy.y + enemy.height and
             player.y + player.height > enemy.y):
            print("Game Over! Final Score:", player.score)
            running = False

    # Update camera
    camera.update(player)
    
    # Draw everything
    screen.fill(BLACK)
    
    # Draw background elements
    for x in range(0, LEVEL_WIDTH, WIDTH):
        bg_rect = pygame.Rect(x - camera.camera.x, 0, WIDTH, HEIGHT)
        if bg_rect.right > 0 and bg_rect.left < WIDTH:
            pygame.draw.rect(screen, (50, 50, 50), bg_rect)
    
    # Draw game objects
    for platform in platforms:
        platform.draw(screen, camera)
    
    for enemy in enemies:
        enemy.draw(screen, camera)
    
    player.draw(screen, camera)
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
