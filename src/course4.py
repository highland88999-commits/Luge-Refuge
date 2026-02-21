import pygame
import sys
import math
import random  # For energy surges simulation

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
PHANTOM_GRAY = (100, 100, 100, 128)  # Semi-transparent

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 4: Quantum Drop Shaft")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# For animation (energy surges)
surge_timer = 0

def draw_track():
    global surge_timer
    surge_timer += 1
    # Draw background - subterranean haze with energy crackles
    screen.fill(DARK_BG)
    for y in range(0, SCREEN_HEIGHT, 10):
        alpha = int(30 * (y / SCREEN_HEIGHT))
        pygame.draw.line(screen, (alpha, 0, alpha + 10), (0, y), (SCREEN_WIDTH, y), 1)
    
    # Draw abandoned maintenance tunnels (vertical shafts as lines/rects)
    pygame.draw.rect(screen, NEON_BLUE, (150, 0, 50, SCREEN_HEIGHT), 2)
    pygame.draw.rect(screen, NEON_PINK, (600, 0, 50, SCREEN_HEIGHT), 2)
    
    # Draw server farms (grid of small rects)
    for x in range(50, 150, 20):
        for y in range(100, 500, 50):
            pygame.draw.rect(screen, AI_RED, (x, y, 15, 15), 1)
    for x in range(650, 750, 20):
        for y in range(100, 500, 50):
            pygame.draw.rect(screen, AI_RED, (x, y, 15, 15), 1)
    
    # Draw the track: mild turn, steep drop, mild turn
    track_width = 200
    start_x = (SCREEN_WIDTH - track_width) // 2
    points = []
    
    # First mild left turn
    section_length = SCREEN_HEIGHT // 4
    for i in range(0, section_length, 10):
        curve_x = start_x + track_width // 2 - int(100 * math.sin(math.pi * i / section_length))
        points.append((curve_x, i))
    
    # Steep drop (near-vertical, minimal horizontal change)
    drop_start_y = section_length
    drop_length = section_length * 2  # Longer for 10m drop representation
    for i in range(0, drop_length, 5):  # Closer points for steepness
        drop_x = points[-1][0] + random.randint(-5, 5)  # Slight wobble for energy surge
        points.append((drop_x, drop_start_y + i))
    
    # Second mild right turn
    turn_start_y = drop_start_y + drop_length
    remaining_length = SCREEN_HEIGHT - turn_start_y
    for i in range(0, remaining_length, 10):
        curve_x = points[-1][0] + int(100 * math.sin(math.pi * i / remaining_length))
        points.append((curve_x, turn_start_y + i))
    
    # Draw the track surface
    pygame.draw.lines(screen, GLOW_GREEN, False, points, track_width)
    
    # Add energy surges (flashing lines along drop)
    if surge_timer % 20 < 10:  # Blink effect
        for i in range(len(points)):
            if drop_start_y < points[i][1] < drop_start_y + drop_length:
                pygame.draw.line(screen, ENERGY_YELLOW, (points[i][0] - track_width // 2 + random.randint(0, track_width), points[i][1]), (points[i][0] - track_width // 2 + random.randint(0, track_width), points[i][1]), 2)
    
    # Draw derelict orbital elevator launch platform at top
    pygame.draw.rect(screen, NEON_PINK, (start_x - 50, 0, track_width + 100, 50), 5)
    
    # AR phantoms (semi-transparent ellipses)
    s = pygame.Surface((50, 100), pygame.SRCALPHA)
    pygame.draw.ellipse(s, PHANTOM_GRAY, (0, 0, 50, 100))
    screen.blit(s, (200, 250))
    screen.blit(s, (550, 350))
    
    # Quantum entanglement displays (small_font text)
    quantum_text = small_font.render("Entangled Data: 101010", True, HOLO_PURPLE)
    screen.blit(quantum_text, (100, 400))
    screen.blit(quantum_text, (600, 450))
    
    # Text overlays for theme
    title_text = font.render("Quantum Drop Shaft", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 600m | Drop: 50m | Turns: 2 | Max Speed: 70 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Novice drop in cybernetic hive-city shafts", True, WHITE)
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
