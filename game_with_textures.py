import pygame
import random
import math
import sys
sys.path.append('.')
from src.constants import *

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")

# Set up directories
GAME_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(GAME_DIR, 'images')

# Load background
background = pygame.image.load(os.path.join(IMAGE_DIR, 'backgrownd.jpg'))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load building textures
building_textures = [
    pygame.image.load(os.path.join(IMAGE_DIR, 'city', 'home1.png')),
    pygame.image.load(os.path.join(IMAGE_DIR, 'city', 'home2.png'))
]
building_textures = [pygame.transform.scale(tex, (PLATFORM_WIDTH, PLATFORM_HEIGHT)) for tex in building_textures]

# Load enemy texture
enemy_texture = pygame.image.load(os.path.join(IMAGE_DIR, 'enemies', 'robot_flor.png'))
enemy_texture = pygame.transform.scale(enemy_texture, (ENEMY_WIDTH, ENEMY_HEIGHT))

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
        self.death_frame = 0
        self.attack_timer = 0
        self.death_timer = 0
        
        # Load animations
        self.animations = {
            'right': [],
            'left': [],
            'jump_right': [],
            'jump_left': [],
            'attack_right': [],
            'attack_left': [],
            'dead': []
        }
        
        # Load walk animations
        for i in range(1, 9):
            img = pygame.image.load(f'images/player_right/player_right{i}.png')
            img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.animations['right'].append(img)
            
            img = pygame.image.load(f'images/player_left/player_left{i}.png')
            img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.animations['left'].append(img)
        
        # Load jump animations
        for i in range(1, 10):
            img = pygame.image.load(f'images/player_jump/player_jump_right/Jump_right{i}.png')
            img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.animations['jump_right'].append(img)
            
            img = pygame.image.load(f'images/player_jump/player_jump_left/Jump_left{i}.png')
            img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.animations['jump_left'].append(img)
            
        # Load attack animations
        for i in range(1, 5):
            img = pygame.image.load(f'images/player_Attack/Attak_right/Attack{i}right.png')
            img = pygame.transform.scale(img, (PLAYER_WIDTH * 1.5, PLAYER_HEIGHT))
            self.animations['attack_right'].append(img)
            
            img = pygame.image.load(f'images/player_Attack/Attak_left/Attack{i}left.png')
            img = pygame.transform.scale(img, (PLAYER_WIDTH * 1.5, PLAYER_HEIGHT))
            self.animations['attack_left'].append(img)
            
        # Load death animations
        for i in range(1, 7):
            img = pygame.image.load(f'images/player_dead/Dead{i}.png')
            img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.animations['dead'].append(img)
            
        # Current image
        self.current_image = self.animations['right'][0]
    
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
    
    def move(self):
        if self.is_dead:
            return
            
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
    
    def update_animation(self):
        if self.is_dead:
            # Update death animation
            self.death_timer += DEATH_ANIMATION_SPEED
            if self.death_timer >= 1:
                self.death_timer = 0
                if self.death_frame < len(self.animations['dead']) - 1:
                    self.death_frame += 1
            self.current_image = self.animations['dead'][self.death_frame]
            return
        
        if self.is_attacking:
            # Update attack animation
            self.attack_timer += ATTACK_ANIMATION_SPEED
            if self.attack_timer >= 1:
                self.attack_timer = 0
                self.attack_frame += 1
                if self.attack_frame >= len(self.animations['attack_right']):
                    self.attack_frame = 0
                    self.is_attacking = False
            
            if self.facing_right:
                self.current_image = self.animations['attack_right'][self.attack_frame]
            else:
                self.current_image = self.animations['attack_left'][self.attack_frame]
            return
            
        if self.jumping:
            # Use jump animation
            frame = int(self.animation_timer * 4) % len(self.animations['jump_right'])
            if self.facing_right:
                self.current_image = self.animations['jump_right'][frame]
            else:
                self.current_image = self.animations['jump_left'][frame]
            self.animation_timer += self.animation_speed
        else:
            # Update walk animation
            if abs(self.vel_x) > 0:
                self.animation_timer += self.animation_speed
                if self.animation_timer >= 1:
                    self.animation_timer = 0
                    self.animation_frame = (self.animation_frame + 1) % 8
                    
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
    
    def draw(self, screen):
        # Update animation
        self.update_animation()
        
        # Draw player sprite
        screen.blit(self.current_image, (self.x, self.y))
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))

class Platform:
    def __init__(self, x, y, width, texture_index=0):
        self.x = x
        self.y = y
        self.width = PLATFORM_WIDTH
        self.height = PLATFORM_HEIGHT
        self.texture = building_textures[texture_index]

    def draw(self, screen):
        screen.blit(self.texture, (self.x, self.y))

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.speed = ENEMY_SPEED
        self.direction = 1
        self.alive = True
        self.initial_x = x
        self.patrol_range = ENEMY_PATROL_RANGE

    def move(self, player):
        if not self.alive:
            return
            
        # Patrol back and forth
        if abs(self.x - self.initial_x) > self.patrol_range:
            self.direction *= -1
        self.x += self.speed * self.direction

    def draw(self, screen):
        if not self.alive:
            return
        screen.blit(enemy_texture, (self.x, self.y))

# Create game objects
player = Player(WIDTH // 2, HEIGHT - PLAYER_HEIGHT)
platforms = [
    Platform(100, HEIGHT - 150, PLATFORM_WIDTH, 0),
    Platform(400, HEIGHT - 250, PLATFORM_WIDTH, 1),
    Platform(700, HEIGHT - 350, PLATFORM_WIDTH, 0),
    Platform(200, HEIGHT - 450, PLATFORM_WIDTH, 1)
]
enemies = [
    Enemy(100, HEIGHT - 200),
    Enemy(600, HEIGHT - 400)
]

# Game states
game_state = PLAYING
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN and game_state == PLAYING:
            if event.key == pygame.K_SPACE and not player.jumping:
                player.vel_y = player.jump_power
                player.jumping = True
                player.on_ground = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == PLAYING:
            if event.button == 1:  # Left mouse button
                player.start_attack()
                # Check for enemy hits
                for enemy in enemies:
                    if not enemy.alive:
                        continue
                    # Check if enemy is in attack range
                    attack_range = ATTACK_RANGE if player.facing_right else -ATTACK_RANGE
                    if ((player.facing_right and enemy.x > player.x and enemy.x < player.x + ATTACK_RANGE) or
                        (not player.facing_right and enemy.x < player.x and enemy.x > player.x - ATTACK_RANGE)):
                        if abs(enemy.y - player.y) < PLAYER_HEIGHT:
                            enemy.alive = False
                            player.score += 100

    # Handle player movement
    if game_state == PLAYING and not player.is_dead:
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
        if not player.is_attacking:
            for enemy in enemies:
                if not enemy.alive:
                    continue
                    
                if (player.x < enemy.x + enemy.width and
                    player.x + player.width > enemy.x and
                    player.y < enemy.y + enemy.height and
                    player.y + player.height > enemy.y):
                    if not player.is_dead:
                        player.start_death()
                        game_state = DYING

    # Draw everything
    screen.fill(BLACK)
    
    # Draw background
    screen.blit(background, (0, 0))
    
    # Draw platforms
    for platform in platforms:
        platform.draw(screen)
    
    # Draw enemies
    for enemy in enemies:
        enemy.draw(screen)
    
    # Draw player
    player.draw(screen)
    
    # Check if death animation is complete
    if game_state == DYING and player.death_frame == len(player.animations['dead']) - 1:
        game_state = GAME_OVER
    
    # Draw game over
    if game_state == GAME_OVER:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over!", True, RED)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, text_rect)
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
