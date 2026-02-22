import pygame
import sys
import math
import random  # For lightning arcs and surge particles

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors for cyberpunk aesthetic
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
DARK_BG = (10, 10, 20)
ZEUS_GOLD = (255, 215, 0, 200)  # Semi-transparent gold
LIGHTNING_WHITE = (255, 255, 255, 180)
SURGE_BLUE = (0, 191, 255, 128)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 9: Cyber Zeus ($2.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 112  # Pixels for visualization
SLED_WIDTH = 45
SLED_COLOR = ZEUS_GOLD

# Lightning arcs and surge particles
arc_timer = 0
surge_particles = []

def add_surge_particles(x, y):
    for _ in range(6):
        surge_particles.append([x + random.randint(-SLED_LENGTH // 2, SLED_LENGTH // 2), y + random.randint(-SLED_WIDTH // 2, SLED_WIDTH // 2), random.randint(2, 5), random.randint(50, 100), SURGE_BLUE])

def update_surge_particles():
    global arc_timer
    arc_timer += 1
    for p in surge_particles[:]:
        p[0] += random.randint(-2, 2)
        p[1] += random.randint(-1, 1)
        p[4] = list(p[4])
        p[4][3] -= 3  # Fade
        if p[4][3] <= 0:
            surge_particles.remove(p)

# Track simulation for auto-call (stormy, charged path for boost demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(95 * math.sin(2 * math.pi * i / SCREEN_HEIGHT)) + random.randint(-15, 15)  # Storm turbulence
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Electrified chassis
    chassis_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(chassis_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(chassis_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Bolt engravings
    for bolt in range(3):
        bolt_x = pos_x - SLED_LENGTH // 2 + 30 + bolt * 30
        bolt_y = pos_y
        pygame.draw.line(screen, LIGHTNING_WHITE[:3], (bolt_x, bolt_y - 15), (bolt_x + 10, bolt_y), 3)
        pygame.draw.line(screen, LIGHTNING_WHITE[:3], (bolt_x + 10, bolt_y), (bolt_x, bolt_y + 15), 3)
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add surges if crackling
    if arc_timer % 12 < 6:
        add_surge_particles(pos_x, pos_y)
    
    # Crackling arcs (random lines)
    if arc_timer % 8 < 4:
        start_x = pos_x + random.randint(-SLED_LENGTH // 2, SLED_LENGTH // 2)
        start_y = pos_y + random.randint(-SLED_WIDTH // 2, SLED_WIDTH // 2)
        end_x = start_x + random.randint(-20, 20)
        end_y = start_y + random.randint(-20, 20)
        pygame.draw.line(screen, LIGHTNING_WHITE[:3], (start_x, start_y), (end_x, end_y), 2)
        branch_x = end_x + random.randint(-10, 10)
        branch_y = end_y + random.randint(-10, 10)
        pygame.draw.line(screen, LIGHTNING_WHITE[:3], (end_x, end_y), (branch_x, branch_y), 1)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw stormy track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 15) % len(track_points)  # Powerful speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update surges
    update_surge_particles()
    for p in surge_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Premium Bobsled 9: Cyber Zeus", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4.5m | Weight: 218kg | Capacity: 4 | Boost: +12 km/h storms", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $2.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Lightning surges +12 km/h storms | Auto-called to tracks", True, WHITE)
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
