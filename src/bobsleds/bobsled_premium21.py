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
OLYMPUS_GOLD = (255, 215, 0, 200)  # Semi-transparent divine armor
RUNE_BLUE = (0, 128, 255, 180)
AURA_YELLOW = (255, 255, 0, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 21: Olympus Eternal ($13.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)
rune_font = pygame.font.SysFont('arial', 12, bold=True)  # Sim rune

# Bobsled parameters
SLED_LENGTH = 127  # Pixels for visualization
SLED_WIDTH = 51
SLED_COLOR = OLYMPUS_GOLD

# Rune pulses and aura particles
rune_timer = 0
aura_particles = []

def add_aura_particles(x, y):
    for _ in range(6):
        aura_particles.append([x + random.randint(-SLED_LENGTH // 2, SLED_LENGTH // 2), y + random.randint(-SLED_WIDTH // 2, SLED_WIDTH // 2), random.randint(3, 6), random.randint(60, 120), AURA_YELLOW])

def update_aura_particles():
    global rune_timer
    rune_timer += 1
    for p in aura_particles[:]:
        p[0] += math.cos(rune_timer / 10 + p[0]) * 0.5  # Gentle orbit
        p[1] += math.sin(rune_timer / 10 + p[1]) * 0.5
        p[4] = list(p[4])
        p[4][3] -= 2  # Slow fade
        if p[4][3] <= 0:
            aura_particles.remove(p)

# Track simulation for auto-call (all-terrain mixed path for mastery demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(100 * math.sin(2 * math.pi * i / SCREEN_HEIGHT)) + random.randint(-20, 20)  # Mixed terrain
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Golden armor hull
    hull_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(hull_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(hull_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Eternal runes (pulsing)
    rune_alpha = 180 + int(75 * math.sin(rune_timer / 12))
    rune_color = (RUNE_BLUE[0], RUNE_BLUE[1], RUNE_BLUE[2], rune_alpha)
    rune_text = rune_font.render("Ω", True, rune_color[:3])  # Omega symbol for eternal
    screen.blit(rune_text, (pos_x - 10, pos_y - 10))
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add aura particles
    add_aura_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw mixed track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 15) % len(track_points)  # Eternal speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update aura
    update_aura_particles()
    for p in aura_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Premium Bobsled 21: Olympus Eternal", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 5.1m | Weight: 260kg | Capacity: 4 | Boost: All-terrain +15 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $13.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("God armor all-terrain mastery | Auto-called to tracks", True, WHITE)
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
