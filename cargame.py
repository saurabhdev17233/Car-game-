import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game Window
WIDTH, HEIGHT = 500, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game - Multi Level")

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)

# Car
car_width, car_height = 50, 80
car = pygame.Rect(WIDTH // 2 - car_width // 2, HEIGHT - car_height - 10, car_width, car_height)

# Obstacles
obstacle_width, obstacle_height = 50, 80
obstacles = []

# Font
font = pygame.font.SysFont(None, 40)

# Clock
clock = pygame.time.Clock()

# Game Variables
level = 1
score = 0
speed = 5
obstacle_speed = 5

def draw_window():
    win.fill(GRAY)
    pygame.draw.rect(win, RED, car)

    for obs in obstacles:
        pygame.draw.rect(win, WHITE, obs)

    level_text = font.render(f'Level: {level}', True, WHITE)
    score_text = font.render(f'Score: {score}', True, WHITE)
    win.blit(level_text, (10, 10))
    win.blit(score_text, (10, 50))

    pygame.display.update()

def reset_obstacles():
    obstacles.clear()
    for _ in range(3):
        x = random.randint(0, WIDTH - obstacle_width)
        y = random.randint(-600, -100)
        obstacles.append(pygame.Rect(x, y, obstacle_width, obstacle_height))

def next_level():
    global level, obstacle_speed, speed
    level += 1
    obstacle_speed += 2
    speed += 1
    reset_obstacles()

def game_over():
    over_text = font.render("Game Over! Press R to Restart", True, WHITE)
    win.blit(over_text, (50, HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(2000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return

def main():
    global score
    reset_obstacles()
    running = True
    while running:
        clock.tick(60)
        draw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Car Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car.left > 0:
            car.x -= speed
        if keys[pygame.K_RIGHT] and car.right < WIDTH:
            car.x += speed

        # Move Obstacles
        for obs in obstacles:
            obs.y += obstacle_speed
            if obs.colliderect(car):
                game_over()
                main()
            if obs.top > HEIGHT:
                obs.x = random.randint(0, WIDTH - obstacle_width)
                obs.y = random.randint(-600, -100)
                score += 1
                if score % 10 == 0:
                    next_level()

    pygame.quit()

if __name__ == "__main__":
    main()
