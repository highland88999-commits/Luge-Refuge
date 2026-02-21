import pygame
import sys
import math
import random  # For anti-grav pulses and distortions

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors for cyberpunk aesthetic
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
DARK_BG = (10, 10, 20)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
HOLO_PURPLE = (200, 0, 255)
AI_RED = (255, 50, 50)
ENERGY_YELLOW = (255, 255, 0)
LASER_ORANGE = (255, 165, 0)
FOG_GRAY = (50, 50, 50, 80)  # Semi-transparent for fog
GRAV_BLUE = (0, 100, 255, 128)  # For anti-grav fields

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 6: Augmented Hump Labyrinth")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# For animation (anti-grav pulses and holographic distortions)
pulse_timer = 0

def draw_track():
    global pulse_timer
    pulse_timer += 1
    # Draw background - neon twilight fog (semi-transparent overlay with gradient)
    screen.fill(DARK_BG)
    fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for y in range(SCREEN_HEIGHT):
        alpha = int(80 * (y / SCREEN_HEIGHT))
        pygame.draw.line(fog_surface, (FOG_GRAY[0], FOG_GRAY[1], FOG_GRAY[2], alpha), (0, y), (SCREEN_WIDTH, y), 1)
    screen.blit(fog_surface, (0, 0))
    
    # Draw derelict sky-scrapers (tall rects with windows)
    for x in [100, 650]:
        pygame.draw.rect(screen, NEON_BLUE, (x, 50, 80, 500), 2)
        for wy in range(100, 500, 30):
            pygame.draw.rect(screen, ENERGY_YELLOW, (x + 10, wy, 20, 10), 1)
    
    # Draw elevated sky-bridges (horizontal lines connecting structures)
    pygame.draw.line(screen, HOLO_PURPLE, (0, 100), (SCREEN_WIDTH, 100), 3)
    pygame.draw.line(screen, HOLO_PURPLE, (0, 400), (SCREEN_WIDTH, 400), 3)
    
    # Draw corrupted ad holograms (semi-transparent rects with text)
    holo_surface = pygame.Surface((150, 80), pygame.SRCALPHA)
    pygame.draw.rect(holo_surface, (NEON_PINK + (128,)), (0, 0, 150, 80), 2)
    ad_text = small_font.render("Buy Neural Upgrades!", True, WHITE)
    holo_surface.blit(ad_text, (10, 30))
    screen.blit(holo_surface, (200, 150))
    screen.blit(holo_surface, (450, 350))
    
    # Draw the track: 4 turns with minor uphill humps (sinusoidal vertical variations)
    track_width = 200
    start_x = (SCREEN_WIDTH - track_width) // 2
    points = []
    y_pos = 0
    section_length = SCREEN_HEIGHT // 5
    
    # Intro straight
    for i in range(0, section_length // 2, 10):
        points.append((start_x + track_width // 2, y_pos))
        y_pos += 10
    
    # Turn 1: Left curve with hump (add sin to y for hump)
    for i in range(0, section_length, 10):
        curve_x = points[-1][0] - int(120 * math.sin(math.pi * i / section_length))
        hump_y = y_pos + int(30 * math.sin(2 * math.pi * i / section_length))  # Hump up and down
        points.append((curve_x, hump_y))
        y_pos = hump_y + 10
    
    # Turn 2: Right curve with hump
    for i in range(0, section_length, 10):
        curve_x = points[-1][0] + int(120 * math.sin(math.pi * i / section_length))
        hump_y = y_pos + int(30 * math.sin(2 * math.pi * i / section_length))
        points.append((curve_x, hump_y))
        y_pos = hump_y + 10
    
    # Turn 3: Left curve with hump
    for i in range(0, section_length, 10):
        curve_x = points[-1][0] - int(120 * math.sin(math.pi * i / section_length))
        hump_y = y_pos + int(30 * math.sin(2 * math.pi * i / section_length))
        points.append((curve_x, hump_y))
        y_pos = hump_y + 10
    
    # Turn 4: Right curve to finish
    remaining_length = SCREEN_HEIGHT - y_pos
    for i in range(0, remaining_length, 10):
        curve_x = points[-1][0] + int(120 * math.sin(math.pi * i / remaining_length))
        hump_y = y_pos + int(30 * math.sin(2 * math.pi * i / remaining_length))
        points.append((curve_x, hump_y))
        y_pos = hump_y + 10
    
    # Draw the track surface
    pygame.draw.lines(screen, GLOW_GREEN, False, points, track_width)
    
    # Add anti-grav pulses (flashing circles along humps)
    if pulse_timer % 25 < 12:  # Blink effect
        for idx, point in enumerate(points[::15]):
            offset = random.randint(-5, 5) if pulse_timer % 3 == 0 else 0
            pygame.draw.circle(screen, GRAV_BLUE[:3] + (128,), (point[0] + offset, point[1]), 20 + (idx % 3 * 5))
    
    # Draw suspended sky-bridge launch platform at top
    pygame.draw.rect(screen, NEON_PINK, (start_x - 50, 0, track_width + 100, 50), 5)
    # Dangling power conduits (lines)
    for dx in [-100, 100]:
        pygame.draw.line(screen, AI_RED, (start_x + track_width // 2 + dx, 50), (start_x + track_width // 2 + dx + random.randint(-20, 20), 100), 2)
    
    # Surveillance nanites (small dots swarming)
    for _ in range(10):
        nx = 150 + random.randint(0, 500)
        ny = 200 + random.randint(0, 300)
        pygame.draw.circle(screen, LASER_ORANGE, (nx, ny), 3)
    
    # Illusory obstacles (flickering rects)
    if pulse_timer % 40 < 20:
        pygame.draw.rect(screen, (HOLO_PURPLE + (128,)), (300, 250, 50, 50), 0)
        pygame.draw.rect(screen, (HOLO_PURPLE + (128,)), (450, 450, 50, 50), 0)
    
    # Text overlays for theme
    title_text = font.render("Augmented Hump Labyrinth", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 800m | Drop: 70m | Turns: 4 | Max Speed: 80 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Intermediate humps in fractured skyline bridges", True, WHITE)
    screen.blit(desc_text, (10, SCREEN_HEIGHT - 60))

def main():
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        draw_track()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
