import pygame
import sys
import os

# Helper function to get correct resource path
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Not running in a PyInstaller bundle
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

# Add the directory containing main.py to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.constants import *
from src.player.player import Player
from src.world.camera import Camera
from src.world.platform import Platform
from src.enemies.enemy import Enemy
from src.ui.menu import Menu
from src.ui.game_over_fixed import GameOver
from src.ui.win_screen import WinScreen

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
            self.background = pygame.image.load(resource_path(os.path.join('images', 'backgrownd.jpg')))
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except Exception as e:
            print(f"Ошибка при загрузке фона: {e}")
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((50, 50, 50))  # Тёмно-серый фон по умолчанию
        
        # Загрузка текстур платформ с обработкой ошибок
        print("Загрузка текстур платформ...")
        try:
            platform_files = [
                'platform1.png',
                'platform2.png',
                'platform3.png'
            ]
            self.platform_textures = []
            for filename in platform_files:
                try:
                    img_path = resource_path(os.path.join('images', 'city', filename))
                    print(f"Пытаемся загрузить: {img_path}")
                    if os.path.exists(img_path): # This check might be less reliable with _MEIPASS
                        texture = pygame.image.load(img_path)
                        self.platform_textures.append(texture)
                        print(f"Успешно загружена текстура: {filename}")
                except Exception as e:
                    print(f"Не удалось загрузить {filename}: {e}")
            
            if not self.platform_textures:
                raise Exception("Не удалось загрузить ни одной текстуры платформы")

            # Масштабируем загруженные текстуры
            self.platform_textures = [pygame.transform.scale(tex, (PLATFORM_WIDTH, PLATFORM_HEIGHT)) for tex in self.platform_textures]
            print(f"Текстуры успешно масштабированы, загружено {len(self.platform_textures)} текстур")

        except Exception as e:
            print(f"Ошибка при загрузке/масштабировании текстур платформ: {e}")
            # Создаем текстуры по умолчанию если не удалось загрузить файлы
            print("Создаем текстуры по умолчанию...")
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
        self.win_screen = WinScreen()
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
            Enemy(2000, HEIGHT - 80),            Enemy(2400, HEIGHT - 340),
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
                elif self.game_state == WIN and self.win_screen.handle_click(event.pos):
                    print("Starting a new game after win")
                    self.reset_game()
                
            # Обновляем состояние кнопок для эффекта наведения
            mouse_pos = pygame.mouse.get_pos()
            if self.game_state == MENU:
                self.menu.start_button.update(mouse_pos)
            elif self.game_state == GAME_OVER:
                self.game_over_screen.retry_button.update(mouse_pos)
            elif self.game_state == WIN:
                self.win_screen.retry_button.update(mouse_pos)
            
            if event.type == pygame.KEYDOWN and self.game_state == PLAYING:
                if event.key == pygame.K_SPACE and not self.player.jumping:
                    print("Player jumping")
                    self.player.vel_y = self.player.jump_power
                    self.player.jumping = True
                    self.player.on_ground = False
                # Добавляем обработку атаки по кнопке Q
                elif event.key == pygame.K_q:
                    print("Player attacking")
                    self.player.start_attack()
                    
                    # Проверяем, находятся ли враги в зоне поражения
                    for enemy in self.enemies:
                        if enemy.alive:
                            # Определяем область атаки в зависимости от направления игрока
                            attack_x_min = self.player.x - ATTACK_RANGE if not self.player.facing_right else self.player.x
                            attack_x_max = self.player.x if not self.player.facing_right else self.player.x + self.player.width + ATTACK_RANGE
                            
                            # Проверяем, находится ли враг в зоне атаки
                            if (enemy.x + enemy.width > attack_x_min and 
                                enemy.x < attack_x_max and
                                abs(enemy.y - self.player.y) < PLAYER_HEIGHT):
                                print(f"Enemy hit by attack at {enemy.x},{enemy.y}")
                                enemy.alive = False
                                self.player.score += 100
        
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
                    
                    # Проверяем столкновение с игроком
                    collision_x = (self.player.x + self.player.width > enemy.x and 
                                 self.player.x < enemy.x + enemy.width)
                    collision_y = (self.player.y + self.player.height > enemy.y and 
                                 self.player.y < enemy.y + enemy.height)
                    
                    # При любом касании врага игрок проигрывает
                    if collision_x and collision_y:
                        self.game_state = GAME_OVER
                        print("Game Over - столкновение с врагом!")
              # Проверка достижения конца уровня (правого края)
            if self.player.x > LEVEL_WIDTH - 100:  # Когда игрок почти у правого края уровня
                self.game_state = WIN
                print("Вы прошли уровень и победили!")
                
            # Проверка падения игрока за пределы уровня
            if self.player.y > HEIGHT + 100:  # Если игрок упал ниже экрана
                self.game_state = GAME_OVER
                print("Game Over - падение в пропасть!")

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
        elif self.game_state == WIN:
            self.win_screen.draw(self.screen, self.player.score)
        
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
