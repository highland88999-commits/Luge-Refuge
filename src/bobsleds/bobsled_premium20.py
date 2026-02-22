import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors for cyberpunk aesthetic
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
DARK_BG = (10, 10, 20)
PHANTOM_GRAY = (150, 150, 150, 150)  # Semi-transparent ghost hull
ECHO_BLUE = (0, 128, 255, 64)
FLICKER_WHITE = (255, 255, 255, 128)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 20: Chrono Phantom ($9.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 115  # Pixels for visualization
SLED_WIDTH = 45
SLED_COLOR = PHANTOM_GRAY

# Timeline flicker and echo trails
flicker_timer = 0
echo_trails = []

def add_echo_trails(x, y):
    echo_trails.append([x, y, random.randint(50, 100), ECHO_BLUE])

def update_echo_trails():
    global flicker_timer
    flicker_timer += 1
    for e in echo_trails[:]:
        e[2] -= 2  # Fade
        e[3] = list(e[3])
        e[3][3] -= 2  # Alpha fade
        if e[2] <= 0:
            echo_trails.remove(e)

# Track simulation for auto-call (turn-heavy path for precision demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(115 * math.sin(2.5 * math.pi * i / SCREEN_HEIGHT))  # Tight turns
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Phasing ghost hull with flicker
    alpha = 150 if flicker_timer % 10 < 5 else 100
    hull_color = (PHANTOM_GRAY[0], PHANTOM_GRAY[1], PHANTOM_GRAY[2], alpha)
    hull_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(hull_surf, hull_color[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(hull_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Time-warp fields (flickering circles)
    warp_radius = 25 + int(15 * math.sin(flicker_timer / 12))
    pygame.draw.circle(screen, FLICKER_WHITE[:3], (pos_x, pos_y), warp_radius, 2)
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add echo trails
    add_echo_trails(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw turn track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 15) % len(track_points)  # Temporal speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update echoes
    update_echo_trails()
    for e in echo_trails:
        echo_surf = pygame.Surface((SLED_LENGTH // 2, SLED_WIDTH // 2), pygame.SRCALPHA)
        pygame.draw.rect(echo_surf, e[3][:3], (0, 0, SLED_LENGTH // 2, SLED_WIDTH // 2))
        screen.blit(echo_surf, (e[0] - SLED_LENGTH // 4, e[1] - SLED_WIDTH // 2))
    
    # Text overlays
    title_text = font.render("Premium Bobsled 20: Chrono Phantom", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4.6m | Weight: 225kg | Capacity: 4 | Boost: Time-slow +15 km/h turns", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $9.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Timeline echoes time-slow precision | Auto-called to tracks", True, WHITE)
    screen.blit(desc_text, (10, SCREEN_HEIGHT - 70))

def main():
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        draw_scene()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
