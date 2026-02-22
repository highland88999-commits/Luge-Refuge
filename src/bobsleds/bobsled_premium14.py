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
ENTROPY_BLACK = (20, 20, 20, 200)  # Semi-transparent chaos hull
SWIRL_PURPLE = (128, 0, 128, 128)
BURST_ORANGE = (255, 165, 0, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 14: Entropy Beast ($2.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 115  # Pixels for visualization
SLED_WIDTH = 48
SLED_COLOR = ENTROPY_BLACK

# Swirling patterns and burst particles
swirl_timer = 0
burst_particles = []

def add_burst_particles(x, y):
    for _ in range(8):
        burst_particles.append([x + random.randint(-SLED_LENGTH // 2, SLED_LENGTH // 2), y + random.randint(-SLED_WIDTH // 2, SLED_WIDTH // 2), random.randint(3, 6), random.randint(50, 100), BURST_ORANGE])

def update_burst_particles():
    global swirl_timer
    swirl_timer += 1
    for p in burst_particles[:]:
        p[0] += math.cos(swirl_timer / 10 + p[0]) * 1.5  # Chaotic swirl
        p[1] += math.sin(swirl_timer / 10 + p[1]) * 1.5
        p[4] = list(p[4])
        p[4][3] -= 3  # Fade
        if p[4][3] <= 0:
            burst_particles.remove(p)

# Track simulation for auto-call (unpredictable, grip-variant path for boost demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(105 * math.sin(math.pi * i / SCREEN_HEIGHT)) + random.randint(-30, 30)  # Entropy unpredictability
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Writhing chaos hull
    hull_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(hull_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(hull_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Swirling patterns (lines twisting)
    for s in range(4):
        s_start_x = pos_x - SLED_LENGTH // 2 + s * 30
        s_start_y = pos_y - SLED_WIDTH // 2
        s_end_x = s_start_x + int(20 * math.sin(swirl_timer / 8 + s))
        s_end_y = s_start_y + SLED_WIDTH + int(15 * math.cos(swirl_timer / 8 + s))
        pygame.draw.line(screen, SWIRL_PURPLE[:3], (s_start_x, s_start_y), (s_end_x, s_end_y), 4)
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add bursts randomly
    if random.random() < 0.3:
        add_burst_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw unpredictable track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 16) % len(track_points)  # Chaotic speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update bursts
    update_burst_particles()
    for p in burst_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Premium Bobsled 14: Entropy Beast", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4.6m | Weight: 228kg | Capacity: 4 | Boost: Random +5-15 km/h grip", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $2.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Chaos swirls random grip boosts | Auto-called to tracks", True, WHITE)
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
