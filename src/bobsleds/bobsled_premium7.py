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
VOID_BLACK = (0, 0, 0, 180)  # Semi-transparent void
WHISPER_PURPLE = (128, 0, 255, 96)
SHADOW_GRAY = (50, 50, 50, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 7: Void Whisper ($2.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 105  # Pixels for visualization
SLED_WIDTH = 42
SLED_COLOR = VOID_BLACK

# Void wisp and shadow particles
wisp_timer = 0
wisp_particles = []

def add_wisp_particles(x, y):
    for _ in range(7):
        wisp_particles.append([x + random.randint(-SLED_LENGTH // 2, SLED_LENGTH // 2), y + random.randint(-SLED_WIDTH // 2, SLED_WIDTH // 2), random.randint(3, 6), random.randint(60, 120), WHISPER_PURPLE])

def update_wisp_particles():
    global wisp_timer
    wisp_timer += 1
    for p in wisp_particles[:]:
        p[0] += math.sin(wisp_timer / 10 + p[0]) * 0.5  # Whisper drift
        p[1] += 0.5
        p[4] = list(p[4])
        p[4][3] -= 2  # Slow fade
        if p[4][3] <= 0:
            wisp_particles.remove(p)

# Track simulation for auto-call (jump-heavy path for stability demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
jump_phases = [150, 300, 450]  # Jump start points
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(85 * math.sin(math.pi * i / SCREEN_HEIGHT))
    if i in jump_phases:
        y_pos += 30  # Air gap sim
    track_points.append((curve_x, y_pos))
    y_pos += 10

def draw_bobsled(pos_x, pos_y, angle=0):
    # Abyss hull with camouflage fade
    cloak_alpha = 180 + int(75 * math.sin(wisp_timer / 20))
    cloak_color = (VOID_BLACK[0], VOID_BLACK[1], VOID_BLACK[2], cloak_alpha)
    hull_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(hull_surf, cloak_color[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(hull_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Anti-grav stabilizers (glowing nodes)
    for node in [-25, 25]:
        pygame.draw.circle(screen, SHADOW_GRAY[:3], (pos_x + node, pos_y), 8)
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add wisps
    add_wisp_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw jump track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 15) % len(track_points)  # Graceful speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update wisps
    update_wisp_particles()
    for p in wisp_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Premium Bobsled 7: Void Whisper", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4.2m | Weight: 205kg | Capacity: 4 | Boost: +12 km/h jumps", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $2.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Shadow stability +12 km/h jumps | Auto-called to tracks", True, WHITE)
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
