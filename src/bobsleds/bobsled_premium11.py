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
ORGANIC_RED = (139, 0, 0, 200)  # Semi-transparent veins
GLITCH_GREEN = (0, 255, 0, 128)
HALLUC_PURPLE = (200, 0, 255, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 10: Neural Nightmare ($2.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 110  # Pixels for visualization
SLED_WIDTH = 44
SLED_COLOR = ORGANIC_RED

# Writhing veins and glitch particles
vein_timer = 0
glitch_particles = []

def add_glitch_particles(x, y):
    for _ in range(6):
        glitch_particles.append([x + random.randint(-SLED_LENGTH // 2, SLED_LENGTH // 2), y + random.randint(-SLED_WIDTH // 2, SLED_WIDTH // 2), random.randint(2, 5), random.randint(40, 80), HALLUC_PURPLE])

def update_glitch_particles():
    global vein_timer
    vein_timer += 1
    for p in glitch_particles[:]:
        p[0] += random.randint(-3, 3)  # Erratic move
        p[1] += random.randint(-2, 2)
        p[4] = list(p[4])
        p[4][3] -= 3  # Fade
        if p[4][3] <= 0:
            glitch_particles.remove(p)

# Track simulation for auto-call (chaotic, distorted path for boost demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(100 * math.sin(2.5 * math.pi * i / SCREEN_HEIGHT)) + random.randint(-20, 20)  # Chaotic twists
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Organic-metal hull
    hull_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(hull_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(hull_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Writhing synaptic webs (veins)
    for v in range(4):
        v_start_x = pos_x - SLED_LENGTH // 2 + v * 25
        v_start_y = pos_y
        v_end_x = v_start_x + int(10 * math.sin(vein_timer / 8 + v))
        v_end_y = v_start_y + int(15 * math.cos(vein_timer / 8 + v))
        pygame.draw.line(screen, GLITCH_GREEN[:3], (v_start_x, v_start_y - SLED_WIDTH // 2), (v_end_x, v_end_y + SLED_WIDTH // 2), 3)
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add glitches
    add_glitch_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw chaotic track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 16) % len(track_points)  # Unsettling speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update glitches
    update_glitch_particles()
    for p in glitch_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Premium Bobsled 10: Neural Nightmare", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4.3m | Weight: 210kg | Capacity: 4 | Boost: +10 km/h chaotic", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $2.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Neural glitches +10 km/h chaotic | Auto-called to tracks", True, WHITE)
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
