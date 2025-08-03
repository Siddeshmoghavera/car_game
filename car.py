import pygame
import random
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚗 Car Dodger - Level Edition")

clock = pygame.time.Clock()
FPS = 60

# Load images
car_img = pygame.image.load("car.png")
car_img = pygame.transform.scale(car_img, (50, 100))

enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (150, 100))
road_img = pygame.image.load("road.png")
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

try:
    coin_img = pygame.image.load("coin.png")
    coin_img = pygame.transform.scale(coin_img, (50, 50))
except:
    coin_img = None

# Font
font = pygame.font.SysFont(None, 40)

# Constants
car_speed = 6
car_x = WIDTH // 2 - 25
car_y = HEIGHT - 120
fuel = 100

enemy_x = random.randint(50, WIDTH - 100)
enemy_y = -100
coin_x = random.randint(60, WIDTH - 60)
coin_y = -400
road_y = 0

def show_text(text, x, y, color=(255, 255, 255)):
    screen.blit(font.render(text, True, color), (x, y))

def get_level(score):
    if score < 10:
        return 1, 6, "Level 1: Rookie"
    elif score < 20:
        return 2, 8, "Level 2: Racer"
    else:
        return 3, 10, "Level 3: Pro Driver"

def crash_screen(score):
    screen.fill((0, 0, 0))
    show_text("💥 CRASHED!", 160, 280)
    show_text(f"Your Score: {score}", 160, 320)
    show_text("Press R to Restart or Q to Quit", 80, 360)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def draw_fuel_bar(fuel):
    pygame.draw.rect(screen, (200, 0, 0), (20, 60, 150, 20))
    pygame.draw.rect(screen, (0, 200, 0), (20, 60, int(150 * fuel / 100), 20))
    show_text("Fuel", 20, 30)

def game_loop():
    global car_x, enemy_x, enemy_y, coin_x, coin_y, road_y
    score = 0
    fuel = 100
    car_x = WIDTH // 2 - 25
    enemy_y = -100
    enemy_x = random.randint(50, WIDTH - 100)
    coin_y = -400
    coin_x = random.randint(60, WIDTH - 60)
    road_y = 0
    power_up = False
    power_up_time = 0

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Scroll background
        road_y += 5
        if road_y >= HEIGHT:
            road_y = 0
        screen.blit(road_img, (0, road_y - HEIGHT))
        screen.blit(road_img, (0, road_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 40:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < WIDTH - 90:
            car_x += car_speed
        if keys[pygame.K_SPACE] and not power_up:
            power_up = True
            power_up_time = pygame.time.get_ticks()

        # Power-up boost
        boost = 4 if power_up else 0
        if power_up and pygame.time.get_ticks() - power_up_time > 3000:
            power_up = False

        # Determine level
        level, enemy_speed, level_name = get_level(score)

        # Draw car, enemy, coin
        screen.blit(car_img, (car_x, car_y))
        screen.blit(enemy_img, (enemy_x, enemy_y))
        if coin_img:
            screen.blit(coin_img, (coin_x, coin_y))
        else:
            pygame.draw.circle(screen, (255, 223, 0), (coin_x + 15, coin_y + 15), 15)

        # Move enemy and coin
        enemy_y += enemy_speed + boost
        coin_y += enemy_speed + boost

        # Collision detection
        car_rect = pygame.Rect(car_x, car_y, 50, 100)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, 100, 100)
        coin_rect = pygame.Rect(coin_x, coin_y, 30, 30)

        if car_rect.colliderect(enemy_rect):
            crash_screen(score)

        if car_rect.colliderect(coin_rect):
            fuel = min(100, fuel + 20)
            score += 1
            coin_y = -random.randint(300, 600)
            coin_x = random.randint(50, WIDTH - 50)

        # Respawn enemy and coin
        if enemy_y > HEIGHT:
            enemy_y = -100
            enemy_x = random.randint(50, WIDTH - 100)
            score += 1

        if coin_y > HEIGHT:
            coin_y = -random.randint(300, 600)
            coin_x = random.randint(60, WIDTH - 60)

        # Decrease fuel
        fuel -= 0.05 * (1 + level)
        if fuel <= 0:
            crash_screen(score)

        # HUD
        show_text(f"Score: {score}", 10, 10)
        show_text(level_name, WIDTH - 250, 10)
        draw_fuel_bar(fuel)

        pygame.display.update()
        clock.tick(FPS)

game_loop()
