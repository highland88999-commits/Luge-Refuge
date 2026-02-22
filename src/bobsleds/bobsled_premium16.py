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
QUANTUM_BLUE = (0, 128, 255, 200)  # Semi-transparent shields
PHASE_PURPLE = (200, 0, 255, 128)
WARP_PARTICLE = (255, 255, 255, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 16: Quantum Leviathan ($9.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 125  # Pixels for visualization (larger for leviathan feel)
SLED_WIDTH = 52
SLED_COLOR = QUANTUM_BLUE

# Warping shields and phase particles
warp_timer = 0
phase_particles = []

def add_phase_particles(x, y):
    for _ in range(10):
        phase_particles.append([x + random.randint(-SLED_LENGTH // 2, SLED_LENGTH // 2), y + random.randint(-SLED_WIDTH // 2, SLED_WIDTH // 2), random.randint(2, 5), random.randint(60, 120), WARP_PARTICLE])

def update_phase_particles():
    global warp_timer
    warp_timer += 1
    for p in phase_particles[:]:
        p[0] += math.cos(warp_timer / 12 + p[0]) * 1  # Warp distortion
        p[1] += math.sin(warp_timer / 12 + p[1]) * 1
        p[4] = list(p[4])
        p[4][3] -= 3  # Fade
        if p[4][3] <= 0:
            phase_particles.remove(p)

# Track simulation for auto-call (spiral-heavy path for boost demo)
track_points = []
center_x = SCREEN_WIDTH // 2
y_pos = 0
radius = 150
angle_step = 2 * math.pi / (SCREEN_HEIGHT / 10)
for i in range(0, SCREEN_HEIGHT, 10):
    angle = i * angle_step
    curve_x = center_x + int(radius * math.cos(angle))
    track_points.append((curve_x, i))
    radius -= 0.5  # Inward spiral

def draw_bobsled(pos_x, pos_y, angle=0):
    # Quantum hull
    hull_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(hull_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(hull_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Shimmering shields (rippling circles)
    shield_radius = 30 + int(20 * math.sin(warp_timer / 10))
    pygame.draw.circle(screen, PHASE_PURPLE[:3], (pos_x, pos_y), shield_radius, 3)
    pygame.draw.circle(screen, PHASE_PURPLE[:3], (pos_x, pos_y), shield_radius - 10, 2)
    
    # Runners
    for offset in [-12, 12]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 6))
    
    # Add phase particles
    add_phase_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw spiral track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 14) % len(track_points)  # Massive speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update phase
    update_phase_particles()
    for p in phase_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Premium Bobsled 16: Quantum Leviathan", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 5m | Weight: 250kg | Capacity: 4 | Boost: +20 km/h spirals", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $9.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Quantum shields +20 km/h spirals | Auto-called to tracks", True, WHITE)
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
