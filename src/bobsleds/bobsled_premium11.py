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
RIFT_GRAY = (100, 100, 100, 200)  # Semi-transparent marauder hull
VORTEX_PURPLE = (128, 0, 128, 128)
ENERGY_ORANGE = (255, 165, 0, 64)
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
SLED_COLOR = RIFT_GRAY

# Vortex and energy particles
vortex_timer = 0
energy_particles = []

def add_energy_particles(x, y):
    for _ in range(5):
        energy_particles.append([x + random.randint(-20, 20), y + random.randint(-SLED_WIDTH // 2, SLED_WIDTH // 2), random.randint(2, 4), random.randint(50, 100), ENERGY_ORANGE])

def update_energy_particles():
    global vortex_timer
    vortex_timer += 1
    for p in energy_particles[:]:
        p[0] += math.cos(vortex_timer / 10 + p[0]) * 1  # Swirl in
        p[1] += math.sin(vortex_timer / 10 + p[1]) * 1
        p[4] = list(p[4])
        p[4][3] -= 3  # Fade
        if p[4][3] <= 0:
            energy_particles.remove(p)

# Track simulation for auto-call (distorted, rift-like path for boost demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(100 * math.sin(math.pi * i / SCREEN_HEIGHT)) + random.randint(-25, 25)  # Rift distortions
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Rift harvester hull
    hull_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(hull_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(hull_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Vortex harvesters (side emitters)
    for side in [-1, 1]:
        vort_x = pos_x + side * (SLED_WIDTH // 2 + 10)
        vort_y = pos_y
        vort_radius = 15 + int(10 * math.sin(vortex_timer / 10 + side))
        pygame.draw.circle(screen, VORTEX_PURPLE[:3], (vort_x, vort_y), vort_radius)
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add energy absorption
    add_energy_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw distorted track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 16) % len(track_points)  # Aggressive speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update energy
    update_energy_particles()
    for p in energy_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Premium Bobsled 11: Rift Marauder", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4.5m | Weight: 222kg | Capacity: 4 | Boost: +11 km/h rifts", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $2.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Rift absorption +11 km/h distorted | Auto-called to tracks", True, WHITE)
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
