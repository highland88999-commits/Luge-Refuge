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
TITAN_GRAY = (80, 80, 80, 200)  # Semi-transparent armor
SPARK_YELLOW = (255, 255, 0, 128)
PLATE_RED = (255, 0, 0, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 12: Mech Titan ($2.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 120  # Pixels for visualization
SLED_WIDTH = 50
SLED_COLOR = TITAN_GRAY

# Shifting plates and spark particles
plate_timer = 0
spark_particles = []

def add_spark_particles(x, y):
    for _ in range(7):
        spark_particles.append([x + random.randint(-SLED_LENGTH // 2, SLED_LENGTH // 2), y + random.randint(-SLED_WIDTH // 2, SLED_WIDTH // 2), random.randint(2, 5), random.randint(40, 80), SPARK_YELLOW])

def update_spark_particles():
    global plate_timer
    plate_timer += 1
    for p in spark_particles[:]:
        p[0] += random.randint(-2, 2)
        p[1] += random.randint(-1, 1)
        p[4] = list(p[4])
        p[4][3] -= 4  # Fade
        if p[4][3] <= 0:
            spark_particles.remove(p)

# Track simulation for auto-call (chaotic path for durability demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(110 * math.sin(2 * math.pi * i / SCREEN_HEIGHT)) + random.randint(-30, 30)  # Chaotic bumps
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Layered titanium plating
    plate_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(plate_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    # Shifting plates
    shift_offset = int(10 * math.sin(plate_timer / 10))
    pygame.draw.rect(plate_surf, PLATE_RED[:3], (shift_offset, 0, SLED_LENGTH // 2, SLED_WIDTH))
    screen.blit(plate_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Hydraulic absorbers (joints)
    for joint in [-20, 20]:
        pygame.draw.circle(screen, NEON_PINK, (pos_x + joint, pos_y + 10), 12)
    
    # Runners
    for offset in [-12, 12]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 6))
    
    # Add sparks on "impact"
    if plate_timer % 8 == 0:
        add_spark_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw chaotic track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 18) % len(track_points)  # Heavy speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update sparks
    update_spark_particles()
    for p in spark_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Premium Bobsled 12: Mech Titan", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4.8m | Weight: 240kg | Capacity: 4 | Boost: +15% chaos durability", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $2.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Armor shifts +15% chaos durability | Auto-called to tracks", True, WHITE)
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
