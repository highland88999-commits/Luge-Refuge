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
ABYSS_BLACK = (0, 0, 0, 200)  # Semi-transparent void hull
TENTACLE_GRAY = (50, 50, 50, 180)
INK_PURPLE = (75, 0, 130, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 22: Abyss Sovereign ($13.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 125  # Pixels for visualization
SLED_WIDTH = 50
SLED_COLOR = ABYSS_BLACK

# Writhing tentacles and ink particles
tentacle_timer = 0
ink_particles = []

def add_ink_particles(x, y):
    for _ in range(8):
        ink_particles.append([x + random.randint(-SLED_LENGTH // 2, SLED_LENGTH // 2), y + random.randint(-SLED_WIDTH // 2, SLED_WIDTH // 2), random.randint(3, 6), random.randint(60, 120), INK_PURPLE])

def update_ink_particles():
    global tentacle_timer
    tentacle_timer += 1
    for p in ink_particles[:]:
        p[0] += random.randint(-1, 1)
        p[1] += 1  # Sink down
        p[4] = list(p[4])
        p[4][3] -= 3  # Fade
        if p[4][3] <= 0:
            ink_particles.remove(p)

# Track simulation for auto-call (plunge-heavy path for boost demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(80 * math.sin(math.pi * i / SCREEN_HEIGHT))
    if i % 100 < 50:  # Steep plunges
        y_pos += 15  # Accelerate
    track_points.append((curve_x, y_pos))
    y_pos += 10

def draw_bobsled(pos_x, pos_y, angle=0):
    # Inky void hull
    hull_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(hull_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(hull_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Writhing tentacles
    for t in range(4):
        t_start_x = pos_x - SLED_LENGTH // 2 + t * 30
        t_start_y = pos_y + ( -10 if t % 2 else 10)
        t_end_x = t_start_x + int(25 * math.sin(tentacle_timer / 8 + t))
        t_end_y = t_start_y + int(20 * math.cos(tentacle_timer / 8 + t))
        pygame.draw.line(screen, TENTACLE_GRAY[:3], (t_start_x, t_start_y), (t_end_x, t_end_y), 5)
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add ink particles
    add_ink_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw plunge track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 14) % len(track_points)  # Abyssal speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update ink
    update_ink_particles()
    for p in ink_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Premium Bobsled 22: Abyss Sovereign", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 5m | Weight: 265kg | Capacity: 4 | Boost: +18 km/h plunges", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $13.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Tentacle thrust +18 km/h plunges | Auto-called to tracks", True, WHITE)
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
