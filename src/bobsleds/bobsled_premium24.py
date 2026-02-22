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
EMPEROR_BLACK = (20, 20, 20, 200)  # Semi-transparent chaos hull
CROWN_GOLD = (255, 215, 0, 180)
CHAOS_PARTICLE = (128, 0, 128, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 24: Entropy Emperor ($13.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 132  # Pixels for visualization
SLED_WIDTH = 53
SLED_COLOR = EMPEROR_BLACK

# Crown swirls and chaos particles
crown_timer = 0
chaos_particles = []

def add_chaos_particles(x, y):
    for _ in range(9):
        chaos_particles.append([x + random.randint(-SLED_LENGTH // 2, SLED_LENGTH // 2), y + random.randint(-SLED_WIDTH // 2, SLED_WIDTH // 2), random.randint(3, 6), random.randint(60, 120), CHAOS_PARTICLE])

def update_chaos_particles():
    global crown_timer
    crown_timer += 1
    for p in chaos_particles[:]:
        p[0] += math.cos(crown_timer / 10 + p[0]) * 1.5  # Imperial swirl
        p[1] += math.sin(crown_timer / 10 + p[1]) * 1.5
        p[4] = list(p[4])
        p[4][3] -= 3  # Fade
        if p[4][3] <= 0:
            chaos_particles.remove(p)

# Track simulation for auto-call (chaotic/distorted path for immunity demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(115 * math.sin(2 * math.pi * i / SCREEN_HEIGHT)) + random.randint(-40, 40)  # Heavy distortions
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Chaos emperor hull
    hull_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(hull_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(hull_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Crown motifs (pulsing spikes)
    crown_alpha = 180 + int(75 * math.sin(crown_timer / 12))
    crown_color = (CROWN_GOLD[0], CROWN_GOLD[1], CROWN_GOLD[2], crown_alpha)
    for spike in range(5):
        spike_x = pos_x - SLED_LENGTH // 2 + spike * (SLED_LENGTH // 4)
        spike_y = pos_y - SLED_WIDTH // 2 - 10
        pygame.draw.triangle(screen, crown_color[:3], (spike_x, spike_y), (spike_x + 10, spike_y - 20), (spike_x - 10, spike_y - 20))
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add chaos particles
    add_chaos_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw chaotic track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 15) % len(track_points)  # Emperor speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update chaos
    update_chaos_particles()
    for p in chaos_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Premium Bobsled 24: Entropy Emperor", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 5.3m | Weight: 275kg | Capacity: 4 | Boost: Immunity +20 km/h chaotic", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $13.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Crown chaos full distortion immunity | Auto-called to tracks", True, WHITE)
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
