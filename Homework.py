import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alien Shoot Game")

# Game settings
player_speed = 5
bullet_speed = 7
alien_speed = 2
spawn_interval = 30  # Frames between alien spawns

# Player
player_width = 50
player_height = 30
player_x = (SCREEN_WIDTH - player_width) // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

# Lists to hold bullets and aliens
bullets = []
aliens = []

# Load fonts
font = pygame.font.Font(None, 36)

# Variables to manage time and score
clock = pygame.time.Clock()
spawn_timer = 0
score = 0

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
        player_rect.x += player_speed
    if keys[pygame.K_SPACE]:
        # Shoot a bullet
        if len(bullets) < 10:  # Limit the number of bullets on screen
            bullet_rect = pygame.Rect(player_rect.centerx - 2, player_rect.top - 10, 4, 10)
            bullets.append(bullet_rect)

    # Update bullets
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)
    
    # Spawn aliens
    spawn_timer += 1
    if spawn_timer >= spawn_interval:
        spawn_timer = 0
        alien_x = random.randint(0, SCREEN_WIDTH - 40)
        alien_rect = pygame.Rect(alien_x, 0, 40, 30)
        aliens.append(alien_rect)

    # Update aliens
    for alien in aliens[:]:
        alien.y += alien_speed
        if alien.y > SCREEN_HEIGHT:
            aliens.remove(alien)  # Remove alien if it goes off-screen
    
    # Collision detection
    for bullet in bullets[:]:
        for alien in aliens[:]:
            if bullet.colliderect(alien):
                bullets.remove(bullet)
                aliens.remove(alien)
                score += 1
                break  # Exit inner loop to avoid modifying lists in nested loops
    
    # Drawing everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, player_rect)  # Draw player
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)  # Draw bullets
    for alien in aliens:
        pygame.draw.rect(screen, RED, alien)  # Draw aliens

    # Display score
    draw_text(f'Score: {score}', font, WHITE, screen, 10, 10)

    pygame.display.flip()
    clock.tick(60)  # Limit FPS to 60


