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
PHANTOM_WHITE = (255, 255, 255, 128)  # Semi-transparent
TRAIL_CYAN = (0, 200, 255, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 1: Neon Phantom ($0.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 95  # Pixels for visualization
SLED_WIDTH = 35
SLED_COLOR = PHANTOM_WHITE

# Particle trail for ghostly effect
particles = []

def add_particles(x, y):
    for _ in range(5):
        particles.append([x, y, random.randint(3, 6), random.randint(50, 100), TRAIL_CYAN])

def update_particles():
    for p in particles[:]:
        p[1] += 1  # Fall
        p[4] = list(p[4])  # Make mutable
        p[4][3] -= 2  # Fade alpha
        if p[4][3] <= 0:
            particles.remove(p)

# Track simulation for auto-call (narrow, shadowy path)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 8):  # Tighter for narrow feel
    curve_x = start_x + int(80 * math.sin(1.5 * math.pi * i / SCREEN_HEIGHT))  # Twisty narrow
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Phasing semi-transparent chassis
    chassis_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(chassis_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    pygame.draw.rect(chassis_surf, NEON_BLUE, (10, 5, SLED_LENGTH - 20, SLED_WIDTH - 10), 3)
    screen.blit(chassis_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Phantom eyes/glow
    pygame.draw.circle(screen, NEON_PINK, (pos_x, pos_y - 10), 8)
    pygame.draw.circle(screen, NEON_PINK, (pos_x, pos_y + 10), 8)
    
    # Runners with glow
    for offset in [-8, 8]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 4))
    
    # Add particles for trails
    add_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw narrow shadowy track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 80)  # Narrower track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 12) % len(track_points)  # Fast animation
    sled_x, sled_y = track_points[sled_index]
    # Angle calculation
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update trails
    update_particles()
    
    # Text overlays
    title_text = font.render("Premium Bobsled 1: Neon Phantom", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 3.8m | Weight: 190kg | Capacity: 4 | Boost: +15 km/h shadows", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $0.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Ghostly trails +5% narrow evasion | Auto-called to tracks", True, WHITE)
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
