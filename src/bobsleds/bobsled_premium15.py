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
MERCURY_SILVER = (192, 192, 192, 200)  # Semi-transparent quicksilver
WING_GOLD = (255, 215, 0, 180)
TRAIL_BLUE = (0, 128, 255, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 15: Mega Hermes ($2.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 110  # Pixels for visualization
SLED_WIDTH = 44
SLED_COLOR = MERCURY_SILVER

# Wing unfold and mercury trail
wing_timer = 0
trail_particles = []

def add_trail_particles(x, y):
    for _ in range(5):
        trail_particles.append([x - SLED_LENGTH // 2, y + random.randint(-SLED_WIDTH // 2, SLED_WIDTH // 2), random.randint(2, 4), random.randint(50, 100), TRAIL_BLUE])

def update_trail_particles():
    global wing_timer
    wing_timer += 1
    for p in trail_particles[:]:
        p[0] -= 1  # Trail behind
        p[1] += math.sin(wing_timer / 10 + p[1]) * 0.5  # Wavy mercury flow
        p[4] = list(p[4])
        p[4][3] -= 3  # Fade
        if p[4][3] <= 0:
            trail_particles.remove(p)

# Track simulation for auto-call (windy tunnel path for optimization demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(100 * math.sin(1.5 * math.pi * i / SCREEN_HEIGHT)) + int(40 * math.sin(4 * math.pi * i / SCREEN_HEIGHT))  # Windy swirls
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Quicksilver hull
    hull_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(hull_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(hull_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Unfolding wings (feathers)
    wing_unfold = 20 + int(20 * math.abs(math.sin(wing_timer / 15)))
    for side in [-1, 1]:
        wing_start_x = pos_x - SLED_LENGTH // 2 + 20
        wing_start_y = pos_y + side * 10
        wing_end_x = wing_start_x - side * wing_unfold
        wing_end_y = wing_start_y
        pygame.draw.line(screen, WING_GOLD[:3], (wing_start_x, wing_start_y), (wing_end_x, wing_end_y), 8)
        # Feather tips
        pygame.draw.line(screen, WING_GOLD[:3], (wing_end_x, wing_end_y), (wing_end_x - side * 10, wing_end_y - 10), 4)
        pygame.draw.line(screen, WING_GOLD[:3], (wing_end_x, wing_end_y), (wing_end_x - side * 10, wing_end_y + 10), 4)
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add mercury trails
    add_trail_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw windy track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 14) % len(track_points)  # Swift speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update trails
    update_trail_particles()
    for p in trail_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Premium Bobsled 15: Mega Hermes", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4.4m | Weight: 210kg | Capacity: 4 | Boost: +14 km/h wind tunnels", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $2.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Winged fins +14 km/h wind | Auto-called to tracks", True, WHITE)
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
