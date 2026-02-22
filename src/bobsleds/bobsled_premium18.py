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
WARLORD_RED = (139, 0, 0, 200)  # Semi-transparent scarred armor
THRUSTER_ORANGE = (255, 165, 0, 180)
BLADE_SILVER = (192, 192, 192, 128)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 18: Ares Warlord ($9.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 122  # Pixels for visualization
SLED_WIDTH = 50
SLED_COLOR = WARLORD_RED

# Thruster flames and blade spin
thruster_timer = 0
flame_particles = []

def add_flame_particles(x, y):
    for _ in range(8):
        flame_particles.append([x - SLED_LENGTH // 2, y + random.randint(-SLED_WIDTH // 2, SLED_WIDTH // 2), random.randint(3, 6), random.randint(50, 100), THRUSTER_ORANGE])

def update_flame_particles():
    global thruster_timer
    thruster_timer += 1
    for p in flame_particles[:]:
        p[0] -= 2  # Trail back
        p[1] += random.randint(-1, 1)
        p[4] = list(p[4])
        p[4][3] -= 4  # Fade
        if p[4][3] <= 0:
            flame_particles.remove(p)

# Track simulation for auto-call (chicane/turn-heavy path for boost demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(120 * math.sin(3 * math.pi * i / SCREEN_HEIGHT))  # Tight chicanes
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Scarred armor hull
    hull_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(hull_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(hull_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Blade turrets (spinning)
    spin_angle = thruster_timer * 10 % 360
    for side in [-1, 1]:
        turret_x = pos_x + side * 30
        turret_y = pos_y - 10
        pygame.draw.circle(screen, BLADE_SILVER[:3], (turret_x, turret_y), 15)
        # Blades
        for b in range(3):
            blade_angle = spin_angle + b * 120
            end_x = turret_x + int(15 * math.cos(math.radians(blade_angle)))
            end_y = turret_y + int(15 * math.sin(math.radians(blade_angle)))
            pygame.draw.line(screen, BLADE_SILVER[:3], (turret_x, turret_y), (end_x, end_y), 3)
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add flames from thrusters
    add_flame_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw chicane track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 16) % len(track_points)  # Aggressive speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update flames
    update_flame_particles()
    for p in flame_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Premium Bobsled 18: Ares Warlord", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4.9m | Weight: 245kg | Capacity: 4 | Boost: +18 km/h chicanes", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $9.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Weapon motifs +18 km/h turns | Auto-called to tracks", True, WHITE)
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
