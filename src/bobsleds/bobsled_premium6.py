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
PLASMA_ORANGE = (255, 69, 0, 200)  # Semi-transparent plasma
EMBER_YELLOW = (255, 255, 0, 128)
FLAME_RED = (255, 0, 0, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 6: Plasma Fury ($2.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 112  # Pixels for visualization
SLED_WIDTH = 45
SLED_COLOR = PLASMA_ORANGE

# Flame vent and ember particles
vent_timer = 0
ember_particles = []

def add_ember_particles(x, y):
    for _ in range(8):
        ember_particles.append([x - SLED_LENGTH // 2, y + random.randint(-SLED_WIDTH // 2, SLED_WIDTH // 2), random.randint(2, 5), random.randint(50, 100), EMBER_YELLOW])

def update_ember_particles():
    global vent_timer
    vent_timer += 1
    for p in ember_particles[:]:
        p[0] -= 2  # Trail behind
        p[1] += random.randint(-1, 1)
        p[4] = list(p[4])
        p[4][3] -= 4  # Fade
        if p[4][3] <= 0:
            ember_particles.remove(p)

# Track simulation for auto-call (plunge-heavy path for boost demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(70 * math.sin(math.pi * i / SCREEN_HEIGHT))  # Steep plunges sim
    if i % 100 < 50:  # Drop sections
        y_pos += 15  # Accelerate visual
    track_points.append((curve_x, y_pos))
    y_pos += 10

def draw_bobsled(pos_x, pos_y, angle=0):
    # Fiery chassis
    chassis_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(chassis_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(chassis_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Superheated vents
    for vent in [-20, 20]:
        vent_x = pos_x - SLED_LENGTH // 2 + 10
        vent_y = pos_y + vent
        vent_alpha = 128 + int(128 * math.sin(vent_timer / 10))
        vent_color = (FLAME_RED[0], FLAME_RED[1], FLAME_RED[2], vent_alpha)
        pygame.draw.ellipse(screen, vent_color[:3], (vent_x, vent_y - 5, 80, 10))
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add embers
    add_ember_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw plunge track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 13) % len(track_points)  # Energetic speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update embers
    update_ember_particles()
    for p in ember_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Premium Bobsled 6: Plasma Fury", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4.5m | Weight: 220kg | Capacity: 4 | Boost: +10 km/h plunges", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $2.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Plasma vents +10 km/h plunges | Auto-called to tracks", True, WHITE)
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
