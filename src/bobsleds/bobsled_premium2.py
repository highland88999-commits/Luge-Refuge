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
CIRCUIT_GREEN = (0, 200, 0, 200)  # Semi-transparent circuits
DATA_YELLOW = (255, 255, 0, 128)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 2: Grid Runner ($0.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 102  # Pixels for visualization
SLED_WIDTH = 42
SLED_COLOR = CIRCUIT_GREEN

# Data pulse animation
pulse_timer = 0
data_particles = []

def add_data_particles(x, y):
    for _ in range(3):
        data_particles.append([x, y, random.randint(2, 4), random.randint(30, 80), DATA_YELLOW])

def update_data_particles():
    global pulse_timer
    pulse_timer += 1
    for p in data_particles[:]:
        p[1] -= 1  # Rise up
        p[4] = list(p[4])
        p[4][3] -= 3  # Fade
        if p[4][3] <= 0:
            data_particles.remove(p)

# Track simulation for auto-call (straight-heavy path for boost demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(50 * math.sin(math.pi * i / SCREEN_HEIGHT))  # Mild curves, emphasis on straights
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Circuit-board frame
    frame_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(frame_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    # Circuit lines
    for line in range(5):
        pygame.draw.line(frame_surf, DATA_YELLOW[:3], (0, line * 10), (SLED_LENGTH, line * 10 + math.sin(pulse_timer / 10) * 5), 2)
    screen.blit(frame_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Holographic grid overlay
    grid_alpha = 128 + int(64 * math.sin(pulse_timer / 15))
    grid_color = (NEON_BLUE[0], NEON_BLUE[1], NEON_BLUE[2], grid_alpha)
    pygame.draw.rect(screen, grid_color[:3], (pos_x - 60, pos_y - 20, 120, 40), 2)
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 10, pos_y + offset, SLED_LENGTH - 20, 5))
    
    # Add data particles
    add_data_particles(pos_x, pos_y + SLED_WIDTH // 2)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw track for context
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 18) % len(track_points)  # Moderate speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update particles
    update_data_particles()
    for p in data_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Premium Bobsled 2: Grid Runner", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4.1m | Weight: 205kg | Capacity: 4 | Boost: +8 km/h straights", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $0.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Circuit pulses +8 km/h straights | Auto-called to tracks", True, WHITE)
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
