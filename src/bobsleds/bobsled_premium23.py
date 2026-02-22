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
SOVEREIGN_PURPLE = (128, 0, 128, 200)  # Semi-transparent crown hull
AURA_BLUE = (0, 128, 255, 128)
PULSE_WAVE = (200, 0, 255, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 23: Neural Sovereign ($13.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 130  # Pixels for visualization
SLED_WIDTH = 52
SLED_COLOR = SOVEREIGN_PURPLE

# Aura pulses and wave particles
aura_timer = 0
wave_particles = []

def add_wave_particles(x, y):
    for _ in range(6):
        wave_particles.append([x, y, random.randint(4, 7), random.randint(50, 100), PULSE_WAVE])

def update_wave_particles():
    global aura_timer
    aura_timer += 1
    for p in wave_particles[:]:
        p[2] += 1  # Expand radius
        p[4] = list(p[4])
        p[4][3] -= 2  # Fade
        if p[4][3] <= 0:
            wave_particles.remove(p)

# Track simulation for auto-call (asymmetric biased path for correction demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(120 * math.sin(math.pi * i / SCREEN_HEIGHT)) + i // 20  # Biased shift (e.g., more left)
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Crown hull
    hull_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(hull_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(hull_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Mind-control auras (pulsing circles)
    aura_radius = 30 + int(20 * math.sin(aura_timer / 10))
    pygame.draw.circle(screen, AURA_BLUE[:3], (pos_x, pos_y), aura_radius, 3)
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add pulse waves
    if aura_timer % 15 == 0:
        add_wave_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw asymmetric track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 15) % len(track_points)  # Sovereign speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update waves
    update_wave_particles()
    for p in wave_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2], 1)
    
    # Text overlays
    title_text = font.render("Premium Bobsled 23: Neural Sovereign", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 5.2m | Weight: 270kg | Capacity: 4 | Boost: Asymmetry +20 km/h biased turns", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $13.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Mind auras asymmetry correction | Auto-called to tracks", True, WHITE)
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
