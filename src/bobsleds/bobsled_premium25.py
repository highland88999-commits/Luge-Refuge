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
ODIN_GRAY = (100, 100, 100, 200)  # Semi-transparent raven hull
EYE_BLUE = (0, 128, 255, 180)
SCAN_BEAM = (0, 255, 255, 128)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 25: Multiversal Odin ($13.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 130  # Pixels for visualization
SLED_WIDTH = 52
SLED_COLOR = ODIN_GRAY

# Eye scan and beam particles
scan_timer = 0
beam_particles = []

def add_beam_particles(x, y):
    for _ in range(4):
        beam_particles.append([x, y - 20, random.randint(50, 150), random.randint(30, 60), SCAN_BEAM])

def update_beam_particles():
    global scan_timer
    scan_timer += 1
    for b in beam_particles[:]:
        b[2] -= 5  # Shorten beam
        b[4] = list(b[4])
        b[4][3] -= 5  # Fade
        if b[4][3] <= 0:
            beam_particles.remove(b)

# Track simulation for auto-call (mixed path for predictive demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(110 * math.sin(1.8 * math.pi * i / SCREEN_HEIGHT)) + random.randint(-20, 20)  # Varied terrain
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Raven-winged hull
    hull_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(hull_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(hull_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Central Eye of Wisdom
    eye_alpha = 180 + int(75 * math.sin(scan_timer / 10))
    eye_color = (EYE_BLUE[0], EYE_BLUE[1], EYE_BLUE[2], eye_alpha)
    pygame.draw.circle(screen, eye_color[:3], (pos_x, pos_y), 15)
    
    # Raven feathers (wings)
    for side in [-1, 1]:
        feather_x = pos_x + side * 40
        feather_y = pos_y + 10
        feather_offset = int(10 * math.cos(scan_timer / 8 + side))
        pygame.draw.ellipse(screen, NEON_PINK, (feather_x - 20, feather_y + feather_offset - 10, 40, 20))
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add scan beams
    if scan_timer % 20 == 0:
        add_beam_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw mixed track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 15) % len(track_points)  # Visionary speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update beams
    update_beam_particles()
    for b in beam_particles:
        end_y = b[1] - b[2]
        pygame.draw.line(screen, b[4][:3], (b[0], b[1]), (b[0], end_y), 2)
    
    # Text overlays
    title_text = font.render("Premium Bobsled 25: Multiversal Odin", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 5.2m | Weight: 268kg | Capacity: 4 | Boost: Predictive +18 km/h all", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $13.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Wisdom eye path highlights | Auto-called to tracks", True, WHITE)
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
