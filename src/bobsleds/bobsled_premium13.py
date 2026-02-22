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
PRISM_RAINBOW = [(255, 0, 0, 128), (255, 165, 0, 128), (255, 255, 0, 128), (0, 255, 0, 128), (0, 0, 255, 128), (75, 0, 130, 128)]  # Rainbow prisms
PHANTOM_GRAY = (200, 200, 200, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 13: Holo Mirage ($2.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 102  # Pixels for visualization
SLED_WIDTH = 42
SLED_COLOR = random.choice(PRISM_RAINBOW)  # Changes for prism effect (sim in code)

# Prism refraction and phantom clones
prism_timer = 0
clone_positions = []

def update_clones(pos_x, pos_y):
    if random.random() < 0.1:  # Random spawn clones
        clone_positions.append([pos_x + random.randint(-30, 30), pos_y + random.randint(-20, 20), random.randint(50, 100)])
    for c in clone_positions[:]:
        c[2] -= 2  # Fade lifetime
        if c[2] <= 0:
            clone_positions.remove(c)

# Track simulation for auto-call (illusory, crowded path for evasion demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(95 * math.sin(1.5 * math.pi * i / SCREEN_HEIGHT)) + random.randint(-15, 15)  # Crowded wobbles
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Prismatic mirror hull
    hull_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    color_index = (prism_timer // 10) % len(PRISM_RAINBOW)
    pygame.draw.rect(hull_surf, PRISM_RAINBOW[color_index][:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(hull_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Refraction lines
    for line in range(5):
        line_x = pos_x - SLED_LENGTH // 2 + line * (SLED_LENGTH // 4)
        pygame.draw.line(screen, random.choice(PRISM_RAINBOW)[:3], (line_x, pos_y - SLED_WIDTH // 2), (line_x, pos_y + SLED_WIDTH // 2), 2)
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Update clones
    update_clones(pos_x, pos_y)

def draw_scene():
    global prism_timer
    prism_timer += 1
    screen.fill(DARK_BG)
    # Draw illusory track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 15) % len(track_points)  # Deceptive speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Draw phantom clones
    for c in clone_positions:
        clone_surf = pygame.Surface((SLED_LENGTH // 2, SLED_WIDTH // 2), pygame.SRCALPHA)
        pygame.draw.rect(clone_surf, PHANTOM_GRAY[:3], (0, 0, SLED_LENGTH // 2, SLED_WIDTH // 2))
        screen.blit(clone_surf, (c[0] - SLED_LENGTH // 4, c[1] - SLED_WIDTH // 4))
    
    # Text overlays
    title_text = font.render("Premium Bobsled 13: Holo Mirage", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4.1m | Weight: 202kg | Capacity: 4 | Boost: +10 km/h illusory", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $2.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Holo clones +10 km/h crowded | Auto-called to tracks", True, WHITE)
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
