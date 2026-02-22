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
RUST_BROWN = (139, 69, 19, 200)  # Semi-transparent rust
SCRAP_LIGHT_YELLOW = (255, 255, 0, 128)
DUST_ORANGE = (204, 85, 0, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 5: Dysto Drifter ($0.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 107  # Pixels for visualization
SLED_WIDTH = 45
SLED_COLOR = RUST_BROWN

# Flicker lights and dust particles
flicker_timer = 0
dust_particles = []

def add_dust_particles(x, y):
    for _ in range(5):
        dust_particles.append([x + random.randint(-SLED_LENGTH // 2, SLED_LENGTH // 2), y, random.randint(1, 3), random.randint(50, 100), DUST_ORANGE])

def update_dust_particles():
    global flicker_timer
    flicker_timer += 1
    for p in dust_particles[:]:
        p[0] += random.randint(-1, 1)  # Drift
        p[1] += 1
        p[4] = list(p[4])
        p[4][3] -= 2  # Fade
        if p[4][3] <= 0:
            dust_particles.remove(p)

# Track simulation for auto-call (long flats for endurance demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(60 * math.sin(math.pi * i / SCREEN_HEIGHT))  # Gentle, flat-emphasis
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Patched rust frame
    frame_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(frame_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    # Scrap patches
    pygame.draw.rect(frame_surf, NEON_PINK, (20, 10, 30, 20))
    pygame.draw.rect(frame_surf, NEON_BLUE, (SLED_LENGTH - 50, 5, 40, 25))
    screen.blit(frame_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Flickering salvage lights
    light_alpha = 128 if flicker_timer % 10 < 5 else 64
    light_color = (SCRAP_LIGHT_YELLOW[0], SCRAP_LIGHT_YELLOW[1], SCRAP_LIGHT_YELLOW[2], light_alpha)
    pygame.draw.circle(screen, light_color[:3], (pos_x - SLED_LENGTH // 4, pos_y), 10)
    pygame.draw.circle(screen, light_color[:3], (pos_x + SLED_LENGTH // 4, pos_y), 10)
    
    # Runners
    for offset in [-12, 12]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 6))
    
    # Add dust particles
    add_dust_particles(pos_x, pos_y + SLED_WIDTH // 2)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw endurance track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 20) % len(track_points)  # Steady speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update particles
    update_dust_particles()
    for p in dust_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Premium Bobsled 5: Dysto Drifter", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4.3m | Weight: 215kg | Capacity: 4 | Boost: +10 km/h flats", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $0.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Scrap endurance +10 km/h flats | Auto-called to tracks", True, WHITE)
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
