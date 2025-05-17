import pygame
import sys
import os

# Add the directory containing main.py to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.constants import *
from src.player.player import Player
from src.world.camera import Camera
from src.world.platform import Platform
from src.enemies.enemy import Enemy
from src.ui.menu import Menu
from src.ui.game_over import GameOver

class Game:
    def __init__(self):
        print("Initializing game...")
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Platform Adventure")
        self.clock = pygame.time.Clock()
        self.game_state = MENU
        print(f"Initial game state: {self.game_state}")
        
        # Load background and textures
        print("Загрузка фона...")
        try:
            self.background = pygame.image.load(os.path.join('images', 'backgrownd.jpg'))
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except Exception as e:
            print(f"Ошибка при загрузке фона: {e}")
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((50, 50, 50))  # Тёмно-серый фон по умолчанию
        
        # Загрузка текстур платформ с обработкой ошибок
        print("Загрузка текстур платформ...")
        try:
            platform_files = ['platform1.png', 'platform2.png', 'platform3.png']
            self.platform_textures = []
            root_dir = os.path.dirname(os.path.abspath(__file__))
            
            for filename in platform_files:
                try:
                    img_path = os.path.join(root_dir, 'images', 'city', filename)
                    print(f"Пытаемся загрузить: {img_path}")
                    if os.path.exists(img_path):
                        texture = pygame.image.load(img_path)
                        texture = pygame.transform.scale(texture, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
                        self.platform_textures.append(texture)
                        print(f"Успешно загружена текстура: {filename}")
                    else:
                        print(f"Файл не найден: {img_path}")
                except Exception as e:
                    print(f"Не удалось загрузить {filename}: {e}")
            
            if not self.platform_textures:
                raise Exception("Не удалось загрузить ни одной текстуры платформы")
        except Exception as e:
            print(f"Ошибка при загрузке текстур платформ: {e}")
            # Создаем текстуры по умолчанию
            self.platform_textures = []
            for color in [(0, 255, 0), (0, 200, 0), (0, 150, 0)]:  # Разные оттенки зеленого
                tex = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                tex.fill(color)
                self.platform_textures.append(tex)
            print("Созданы текстуры по умолчанию")
        
        # Create game objects
        self.init_game_objects()
        print("Game objects initialized")
        
        # Create UI elements
        self.menu = Menu()
        self.game_over_screen = GameOver()
        print("UI elements created")

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
        self.enemies = [
            Enemy(400, HEIGHT - 80),
            Enemy(800, HEIGHT - 190),
            Enemy(1200, HEIGHT - 80),
            Enemy(1600, HEIGHT - 290),
            Enemy(2000, HEIGHT - 80),
            Enemy(2400, HEIGHT - 340),
            Enemy(2800, HEIGHT - 290),
        ]

    def reset_game(self):
        self.game_state = PLAYING
        self.init_game_objects()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(f"Mouse click at {event.pos}")
                if self.game_state == MENU and self.menu.handle_click(event.pos):
                    print("Starting game from menu")
                    self.game_state = PLAYING
                elif self.game_state == GAME_OVER and self.game_over_screen.handle_click(event.pos):
                    print("Restarting game from game over")
                    self.reset_game()
            
            if event.type == pygame.KEYDOWN and self.game_state == PLAYING:
                if event.key == pygame.K_SPACE and not self.player.jumping:
                    print("Player jumping")
                    self.player.vel_y = self.player.jump_power
                    self.player.jumping = True
                    self.player.on_ground = False
                elif event.key == pygame.K_q:
                    print("Player attacking")
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

            # Update enemies and check collisions
            for enemy in self.enemies:
                if enemy.alive:
                    enemy.move(self.player)
                    
                    # Check for collision with player
                    if (self.player.x + self.player.width > enemy.x and 
                        self.player.x < enemy.x + enemy.width and
                        self.player.y + self.player.height > enemy.y and
                        self.player.y < enemy.y + enemy.height):
                        if self.player.vel_y > 0:  # Player is jumping on the enemy
                            enemy.alive = False
                            self.player.vel_y = self.player.jump_power
                            self.player.score += 100
                        elif not self.player.is_attacking:  # Player is not attacking
                            print("Player died!")
                            self.game_state = GAME_OVER

            # Update camera
            self.camera.update(self.player)

    def draw(self):
        self.screen.fill(BLACK)

        if self.game_state == MENU:
            self.menu.draw(self.screen)
        elif self.game_state == PLAYING:
            # Draw parallax background
            rel_x = self.camera.camera.x % WIDTH
            self.screen.blit(self.background, (-rel_x, 0))
            if rel_x < WIDTH:
                self.screen.blit(self.background, (WIDTH - rel_x, 0))
            
            # Draw game objects
            for platform in self.platforms:
                platform.draw(self.screen, self.camera)
            
            for enemy in self.enemies:
                enemy.draw(self.screen, self.camera)
            
            self.player.draw(self.screen, self.camera)
        elif self.game_state == GAME_OVER:
            self.game_over_screen.draw(self.screen, self.player.score)
        
        pygame.display.flip()

    def run(self):
        print("Starting game loop...")
        running = True
        try:
            while running:
                running = self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(FPS)
        except Exception as e:
            print(f"Error in game loop: {e}")
        finally:
            print("Exiting game...")
            pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
