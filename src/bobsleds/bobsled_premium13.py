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
RIFT_HULL = (50, 50, 100, 200)  # Semi-transparent rift metal
CLAW_SILVER = (192, 192, 192, 180)
SIPHON_PURPLE = (200, 0, 255, 128)
ENERGY_SPARK = (255, 255, 0, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 11: Rift Marauder ($2.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 112  # Pixels for visualization
SLED_WIDTH = 46
SLED_COLOR = RIFT_HULL

# Claw and siphon particles
claw_timer = 0
spark_particles = []

def add_spark_particles(x, y):
    for _ in range(5):
        spark_particles.append([x, y, random.randint(2, 4), random.randint(50, 100), ENERGY_SPARK])

def update_spark_particles():
    global claw_timer
    claw_timer += 1
    for p in spark_particles[:]:
        p[0] += random.randint(-2, 2)
        p[1] += random.randint(-1, 1)
        p[4] = list(p[4])
        p[4][3] -= 3  # Fade
        if p[4][3] <= 0:
            spark_particles.remove(p)

# Track simulation for auto-call (distorted, rift-like path for boost demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(100 * math.sin(math.pi * i / SCREEN_HEIGHT)) + random.randint(-25, 25)  # Rift distortions
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Rift-claw hull
    hull_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(hull_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(hull_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Jagged claws (appendages)
    claw_length = 25 + int(15 * math.sin(claw_timer / 10))
    for side in [-1, 1]:
        claw_start_x = pos_x + side * (SLED_WIDTH // 2 + 5)
        claw_start_y = pos_y
        claw_end_x = claw_start_x + side * claw_length
        claw_end_y = claw_start_y + math.cos(claw_timer / 8 + side) * 8
        pygame.draw.line(screen, CLAW_SILVER[:3], (claw_start_x, claw_start_y), (claw_end_x, claw_end_y), 5)
    
    # Vortex harvesters
    for side in [-1, 1]:
        vort_x = pos_x + side * 20
        vort_y = pos_y + 15
        pygame.draw.circle(screen, SIPHON_PURPLE[:3], (vort_x, vort_y), 10 + int(5 * math.sin(claw_timer / 12)))
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add sparks
    add_spark_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw rift track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 15) % len(track_points)  # Marauding speed
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
    title_text = font.render("Premium Bobsled 11: Rift Marauder", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4.5m | Weight: 222kg | Capacity: 4 | Boost: +11 km/h rifts", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $2.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Rift claws +11 km/h distorted | Auto-called to tracks", True, WHITE)
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
