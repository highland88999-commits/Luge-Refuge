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
STELLAR_BLACK = (0, 0, 20, 200)  # Semi-transparent void hull
NEBULA_PURPLE = (128, 0, 128, 128)
COMET_WHITE = (255, 255, 255, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 19: Stellar Vortex ($9.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 117  # Pixels for visualization
SLED_WIDTH = 47
SLED_COLOR = STELLAR_BLACK

# Nebula swirls and comet trails
nebula_timer = 0
comet_particles = []

def add_comet_particles(x, y):
    for _ in range(7):
        comet_particles.append([x - SLED_LENGTH // 2, y + random.randint(-SLED_WIDTH // 2, SLED_WIDTH // 2), random.randint(2, 5), random.randint(60, 120), COMET_WHITE])

def update_comet_particles():
    global nebula_timer
    nebula_timer += 1
    for p in comet_particles[:]:
        p[0] -= 3  # Trail behind
        p[1] += random.randint(-1, 1)
        p[4] = list(p[4])
        p[4][3] -= 3  # Fade
        if p[4][3] <= 0:
            comet_particles.remove(p)

# Track simulation for auto-call (jump-heavy path for extension demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(90 * math.sin(math.pi * i / SCREEN_HEIGHT))
    if i % 150 < 50:  # Air gaps for jumps
        y_pos += 20  # Extended air sim
    track_points.append((curve_x, y_pos))
    y_pos += 10

def draw_bobsled(pos_x, pos_y, angle=0):
    # Star-field hull
    hull_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(hull_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(hull_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Nebula swirls (rotating ellipses)
    swirl_radius = 20 + int(10 * math.sin(nebula_timer / 10))
    pygame.draw.ellipse(screen, NEBULA_PURPLE[:3], (pos_x - 30, pos_y - 15, 60, 30))
    pygame.draw.ellipse(screen, NEBULA_PURPLE[:3], (pos_x - 20, pos_y - 20, 40, 40), width=2)
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add comet trails
    add_comet_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw jump track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 15) % len(track_points)  # Cosmic speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update comets
    update_comet_particles()
    for p in comet_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Premium Bobsled 19: Stellar Vortex", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4.7m | Weight: 232kg | Capacity: 4 | Boost: +15 km/h jumps", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $9.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Star glow +15 km/h jumps | Auto-called to tracks", True, WHITE)
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
