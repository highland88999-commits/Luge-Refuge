import pygame
import sys
import math
import random  # For tectonic rumbles, energy discharges, and distortions

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
PLASMA_ORANGE = (255, 69, 0, 128)  # Semi-transparent for plasma
SMOG_GRAY = (50, 50, 50, 100)  # Semi-transparent for smog
NANO_BLUE = (0, 128, 255)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 9: Plasma Steep Ravine")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# For animation (tectonic rumbles, plasma discharges, nanobot swarms)
rumble_timer = 0

def draw_track():
    global rumble_timer
    rumble_timer += 1
    # Draw background - smog-filled void with gradient
    screen.fill(DARK_BG)
    smog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for y in range(SCREEN_HEIGHT):
        alpha = int(100 * (y / SCREEN_HEIGHT))
        pygame.draw.line(smog_surface, (SMOG_GRAY[0], SMOG_GRAY[1], SMOG_GRAY[2], alpha), (0, y), (SCREEN_WIDTH, y), 1)
    screen.blit(smog_surface, (0, 0))
    
    # Draw colossal megastructures (wide vertical walls)
    pygame.draw.rect(screen, NEON_BLUE, (50, 0, 100, SCREEN_HEIGHT), 2)
    pygame.draw.rect(screen, NEON_PINK, (650, 0, 100, SCREEN_HEIGHT), 2)
    
    # Draw plasma-vented fissures (glowing cracks with discharges)
    for y in range(100, SCREEN_HEIGHT, 100):
        pygame.draw.line(screen, PLASMA_ORANGE[:3], (150, y), (250, y + random.randint(-20, 20)), 3)
        pygame.draw.line(screen, PLASMA_ORANGE[:3], (550, y + random.randint(-20, 20)), (650, y), 3)
    if rumble_timer % 15 < 7:  # Flashing discharges
        for _ in range(5):
            dx = random.randint(150, 250)
            dy = random.randint(100, 500)
            pygame.draw.circle(screen, ENERGY_YELLOW, (dx, dy), random.randint(10, 20))
            dx2 = random.randint(550, 650)
            pygame.draw.circle(screen, ENERGY_YELLOW, (dx2, dy), random.randint(10, 20))
    
    # Draw holographic warning beacons (flashing text)
    if rumble_timer % 30 < 15:
        warn_text = small_font.render("WARNING: Tectonic Instability", True, AI_RED)
        screen.blit(warn_text, (200 + random.randint(-5, 5), 250))
        screen.blit(warn_text, (400 + random.randint(-5, 5), 400))
    
    # Draw the track: 7 turns with extended steep drop (minimal turns in drop)
    track_width = 200
    start_x = (SCREEN_WIDTH - track_width) // 2
    points = []
    y_pos = 0
    section_length = SCREEN_HEIGHT // 8
    
    # Pre-drop: 3 mild turns to build up
    # Turn 1: Left
    for i in range(0, section_length, 10):
        curve_x = start_x + track_width // 2 - int(80 * math.sin(math.pi * i / section_length))
        points.append((curve_x, y_pos))
        y_pos += 10
    
    # Turn 2: Right
    for i in range(0, section_length, 10):
        curve_x = points[-1][0] + int(80 * math.sin(math.pi * i / section_length))
        points.append((curve_x, y_pos))
        y_pos += 10
    
    # Turn 3: Left
    for i in range(0, section_length, 10):
        curve_x = points[-1][0] - int(80 * math.sin(math.pi * i / section_length))
        points.append((curve_x, y_pos))
        y_pos += 10
    
    # Extended steep drop: Mostly straight/vertical with 1 minor turn (turn 4)
    drop_length = section_length * 3  # Extended for 20m representation
    drop_start_y = y_pos
    # Minor wiggle for turn 4
    for i in range(0, drop_length // 2, 5):
        drop_x = points[-1][0] + int(50 * math.sin(2 * math.pi * i / drop_length))  # Minor oscillation
        rumble_offset = random.randint(-5, 5) if rumble_timer % 10 < 5 else 0  # Quake effect
        points.append((drop_x + rumble_offset, y_pos))
        y_pos += 10
    for i in range(drop_length // 2, drop_length, 5):
        drop_x = points[-1][0] - int(50 * math.sin(2 * math.pi * i / drop_length))
        rumble_offset = random.randint(-5, 5) if rumble_timer % 10 < 5 else 0
        points.append((drop_x + rumble_offset, y_pos))
        y_pos += 10
    
    # Post-drop: 3 turns for recovery (turns 5-7)
    # Turn 5: Right
    for i in range(0, section_length, 10):
        curve_x = points[-1][0] + int(80 * math.sin(math.pi * i / section_length))
        points.append((curve_x, y_pos))
        y_pos += 10
    
    # Turn 6: Left
    for i in range(0, section_length, 10):
        curve_x = points[-1][0] - int(80 * math.sin(math.pi * i / section_length))
        points.append((curve_x, y_pos))
        y_pos += 10
    
    # Turn 7: Right to finish
    remaining_length = SCREEN_HEIGHT - y_pos
    for i in range(0, remaining_length, 10):
        curve_x = points[-1][0] + int(80 * math.sin(math.pi * i / remaining_length))
        points.append((curve_x, y_pos))
        y_pos += 10
    
    # Draw the track surface
    pygame.draw.lines(screen, GLOW_GREEN, False, points, track_width)
    
    # Add plasma barriers (lines along drop)
    for i in range(len(points)):
        if drop_start_y < points[i][1] < drop_start_y + drop_length:
            pygame.draw.line(screen, PLASMA_ORANGE[:3], (points[i][0] - track_width // 2, points[i][1]), (points[i][0] + track_width // 2, points[i][1]), 2)
    
    # Draw precarious ledge launch platform at top
    pygame.draw.rect(screen, NEON_PINK, (start_x + 50, 0, track_width - 100, 50), 5)  # Narrower for precarious feel
    
    # Rogue nanobot swarms (clusters of moving dots)
    for _ in range(3):
        swarm_x = 300 + random.randint(-100, 100)
        swarm_y = 300 + random.randint(-100, 100) + (rumble_timer % 50) - 25  # Moving
        for n in range(10):
            nx = swarm_x + random.randint(-20, 20)
            ny = swarm_y + random.randint(-20, 20)
            pygame.draw.circle(screen, NANO_BLUE, (nx, ny), 2)
    
    # Text overlays for theme
    title_text = font.render("Plasma Steep Ravine", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 1100m | Drop: 100m | Turns: 7 | Max Speed: 95 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Advanced steep plunge in abyssal megacity ravines", True, WHITE)
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
