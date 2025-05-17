import pygame
import sys
import os

# Add the directory containing main.py to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from src.constants import *
from src.player.player import Player
from src.world.camera import Camera
from src.world.platform import Platform
from src.enemies.enemy import Enemy
from src.ui.menu import Menu
from src.ui.game_over import GameOver

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Platform Adventure")
        self.clock = pygame.time.Clock()
        self.game_state = MENU

        # Set up directories
        self.game_dir = current_dir
        self.image_dir = os.path.join(self.game_dir, 'images')
        
        # Load textures
        self.load_textures()
        
        # Create game objects and UI
        self.init_game_objects()
        self.menu = Menu()
        self.game_over_screen = GameOver()
    
    def load_textures(self):
        # Load background
        self.background = pygame.image.load(os.path.join(self.image_dir, 'backgrownd.jpg'))
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        
        # Load building textures
        self.platform_textures = [
            pygame.image.load(os.path.join(self.image_dir, 'city', 'home1.png')),
            pygame.image.load(os.path.join(self.image_dir, 'city', 'home2.png'))
        ]
        self.platform_textures = [pygame.transform.scale(tex, (PLATFORM_WIDTH, PLATFORM_HEIGHT)) 
                                for tex in self.platform_textures]
        
        # Load enemy texture
        self.enemy_texture = pygame.image.load(os.path.join(self.image_dir, 'enemies', 'robot_flor.png'))
        self.enemy_texture = pygame.transform.scale(self.enemy_texture, (ENEMY_WIDTH, ENEMY_HEIGHT))

    def init_game_objects(self):
        self.player = Player(50, HEIGHT - 100)
        self.camera = Camera(WIDTH, HEIGHT)
        
        # Platform configurations
        platform_configs = [
            # Ground platforms with gaps for challenge
            (0, HEIGHT - 40, 600),
            (700, HEIGHT - 40, 400),
            (1200, HEIGHT - 40, 500),
            (1800, HEIGHT - 40, 400),
            (2300, HEIGHT - 40, 400),
            (2800, HEIGHT - 40, 400),
            
            # Floating platforms
            (300, HEIGHT - 150, 200),
            (600, HEIGHT - 250, 200),
            (900, HEIGHT - 200, 200),
            (1200, HEIGHT - 300, 200),
            (1500, HEIGHT - 250, 200),
            (1800, HEIGHT - 350, 200),
            (2100, HEIGHT - 200, 200),
            (2400, HEIGHT - 300, 200),
            (2700, HEIGHT - 250, 200),
        ]
        
        # Create platforms with textures
        self.platforms = []
        for x, y, width in platform_configs:
            platform = Platform(x, y, width)
            # Alternate between platform textures
            texture = self.platform_textures[len(self.platforms) % len(self.platform_textures)]
            platform.set_texture(texture)
            self.platforms.append(platform)
        
        # Create enemies
        self.enemies = []
        enemy_positions = [
            (400, HEIGHT - 80),
            (800, HEIGHT - 190),
            (1200, HEIGHT - 80),
            (1600, HEIGHT - 290),
            (2000, HEIGHT - 80),
            (2400, HEIGHT - 340),
            (2800, HEIGHT - 290),
        ]
        for x, y in enemy_positions:
            enemy = Enemy(x, y)
            enemy.texture = self.enemy_texture
            self.enemies.append(enemy)

    def reset_game(self):
        self.game_state = PLAYING
        self.init_game_objects()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == MENU and self.menu.handle_click(event.pos):
                    self.game_state = PLAYING
                elif self.game_state == GAME_OVER and self.game_over_screen.handle_click(event.pos):
                    self.reset_game()
                    
            if event.type == pygame.KEYDOWN and self.game_state == PLAYING:
                if event.key == pygame.K_SPACE and not self.player.jumping:
                    self.player.vel_y = self.player.jump_power
                    self.player.jumping = True
                    self.player.on_ground = False
                elif event.key == pygame.K_x:
                    self.player.start_attack()
        
        return True

    def update(self):
        if self.game_state == PLAYING:
            # Handle player movement
            keys = pygame.key.get_pressed()
            self.player.vel_x = 0
            if keys[pygame.K_LEFT]:
                self.player.vel_x = -self.player.speed
                self.player.facing_right = False
            if keys[pygame.K_RIGHT]:
                self.player.vel_x = self.player.speed
                self.player.facing_right = True

            # Update game objects
            self.player.move()
            
            # Platform collision
            self.player.on_ground = False
            for platform in self.platforms:
                if (self.player.y + self.player.height >= platform.y and 
                    self.player.y < platform.y and 
                    self.player.x + self.player.width > platform.x and 
                    self.player.x < platform.x + platform.width):
                    if self.player.vel_y >= 0:
                        self.player.y = platform.y - self.player.height
                        self.player.vel_y = 0
                        self.player.on_ground = True
                        self.player.jumping = False

            # Update enemies
            for enemy in self.enemies:
                enemy.move(self.player)

            # Check for collision with enemies
            for enemy in self.enemies:
                if not enemy.alive:
                    continue
                    
                if (self.player.x + self.player.width > enemy.x and 
                    self.player.x < enemy.x + enemy.width and
                    self.player.y + self.player.height > enemy.y and
                    self.player.y + self.player.height < enemy.y + enemy.height and
                    self.player.vel_y > 0):
                    # Kill enemy and bounce player
                    enemy.alive = False
                    self.player.vel_y = self.player.jump_power
                    self.player.score += 100
                elif (self.player.x < enemy.x + enemy.width and
                     self.player.x + self.player.width > enemy.x and
                     self.player.y < enemy.y + enemy.height and
                     self.player.y + self.player.height > enemy.y):
                    self.game_state = GAME_OVER

            # Update camera
            self.camera.update(self.player)

    def draw(self):
        self.screen.fill(BLACK)
        
        if self.game_state == MENU:
            self.menu.draw(self.screen)
            
        elif self.game_state == PLAYING:
            # Draw background with parallax scrolling
            for x in range(0, LEVEL_WIDTH, WIDTH):
                bg_pos = (x - self.camera.camera.x * 0.5, 0)  # Multiply by 0.5 for parallax effect
                if bg_pos[0] > -WIDTH and bg_pos[0] < WIDTH:
                    self.screen.blit(self.background, bg_pos)
            
            # Draw platforms
            for platform in self.platforms:
                platform.draw(self.screen, self.camera)
            
            # Draw enemies
            for enemy in self.enemies:
                enemy.draw(self.screen, self.camera)
            
            # Draw player
            self.player.draw(self.screen, self.camera)
            
        elif self.game_state == GAME_OVER:
            self.game_over_screen.draw(self.screen, self.player.score)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
