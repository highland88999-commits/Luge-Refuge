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
BLADE_SILVER = (192, 192, 192, 200)  # Semi-transparent blade
RUNE_RED = (255, 0, 0, 128)
SLICE_YELLOW = (255, 255, 0, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 3: Street Samurai ($0.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)
rune_font = pygame.font.SysFont('arial', 10, bold=True)  # Simple rune sim

# Bobsled parameters
SLED_LENGTH = 100  # Pixels for visualization
SLED_WIDTH = 40
SLED_COLOR = BLADE_SILVER

# Slice particle and rune flash
flash_timer = 0
slice_particles = []

def add_slice_particles(x, y):
    for _ in range(4):
        slice_particles.append([x, y, random.randint(4, 7), random.randint(40, 90), SLICE_YELLOW])

def update_slice_particles():
    global flash_timer
    flash_timer += 1
    for p in slice_particles[:]:
        p[0] += random.randint(-2, 2)  # Scatter
        p[1] += 1
        p[4] = list(p[4])
        p[4][3] -= 4  # Fade
        if p[4][3] <= 0:
            slice_particles.remove(p)

# Track simulation for auto-call (jagged, uneven path for grip demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(100 * math.sin(3 * math.pi * i / SCREEN_HEIGHT)) + random.randint(-10, 10)  # Jagged wobble
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Katana blade chassis
    blade_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.polygon(blade_surf, SLED_COLOR[:3], [(0, 0), (SLED_LENGTH, SLED_WIDTH // 2 - 10), (0, SLED_WIDTH)])
    screen.blit(blade_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Glowing samurai runes
    rune_alpha = 128 + int(128 * math.sin(flash_timer / 12))
    rune_color = (RUNE_RED[0], RUNE_RED[1], RUNE_RED[2], rune_alpha)
    rune_text = rune_font.render("侍", True, rune_color[:3])  # Simple samurai symbol
    blade_surf.blit(rune_text, (SLED_LENGTH // 2 - 10, SLED_WIDTH // 2 - 10))
    screen.blit(blade_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Edge blades/runners
    for offset in [-15, 15]:
        pygame.draw.polygon(screen, GLOW_GREEN, [(pos_x - SLED_LENGTH // 2, pos_y + offset), (pos_x + SLED_LENGTH // 2, pos_y + offset), (pos_x + SLED_LENGTH // 2 - 20, pos_y + offset + 5)])
    
    # Add slice particles on turns (sim sharp handling)
    if flash_timer % 10 == 0:
        add_slice_particles(pos_x + SLED_LENGTH // 2, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw jagged track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 16) % len(track_points)  # Dynamic speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update particles
    update_slice_particles()
    for p in slice_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Premium Bobsled 3: Street Samurai", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4m | Weight: 200kg | Capacity: 4 | Boost: +10 km/h jagged", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $0.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Blade grip on jagged +10 km/h | Auto-called to tracks", True, WHITE)
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
