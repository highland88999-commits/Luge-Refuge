import pygame
import sys
import math
import random  # For portal instabilities, energy surges, and illusions

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
PORTAL_BLUE = (0, 255, 255, 128)  # Semi-transparent for portals
STATIC_GRAY = (100, 100, 100, 64)  # For static distortions
DRONE_ORANGE = (255, 140, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 10: Strata Cascade Descent")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# For animation (portal instabilities, energy surges, holographic illusions)
instability_timer = 0

def draw_track():
    global instability_timer
    instability_timer += 1
    # Draw background - perpetual digital eclipse with stratified layers
    screen.fill(DARK_BG)
    # Strata layers (horizontal bands)
    strata_colors = [NEON_BLUE, HOLO_PURPLE, NEON_PINK, AI_RED]
    for i in range(4):
        strata_y = i * (SCREEN_HEIGHT // 4)
        pygame.draw.rect(screen, strata_colors[i % len(strata_colors)], (0, strata_y, SCREEN_WIDTH, SCREEN_HEIGHT // 4), 0)
    
    # Overlay static distortions
    static_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    if instability_timer % 20 < 10:  # Flicker
        for _ in range(50):
            sx = random.randint(0, SCREEN_WIDTH)
            sy = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.line(static_surface, STATIC_GRAY[:3], (sx, sy), (sx + random.randint(-10, 10), sy), 1)
    screen.blit(static_surface, (0, 0))
    
    # Draw cascading data waterfalls (vertical streaming text)
    for x in [100, 700]:
        for y in range(0, SCREEN_HEIGHT, 50):
            offset = (instability_timer % 50) - 25  # Moving down
            pygame.draw.line(screen, ENERGY_YELLOW, (x, y + offset), (x, y + offset + 40), 2)
            data_text = small_font.render("DATA CASCADE 101010", True, ENERGY_YELLOW)
            screen.blit(data_text, (x - 40, y + offset + 10))
    
    # Draw patrolling security drones (moving polygons)
    drone_positions = [(200 + (instability_timer % 200) - 100, 150), (500 - (instability_timer % 200) + 100, 350)]
    for dx, dy in drone_positions:
        drone_points = [(dx, dy), (dx + 20, dy - 20), (dx + 40, dy), (dx + 20, dy + 20)]
        pygame.draw.polygon(screen, DRONE_ORANGE, drone_points)
    
    # Draw lockdown holograms (flashing rects with text)
    if instability_timer % 30 < 15:
        holo_surface = pygame.Surface((150, 80), pygame.SRCALPHA)
        pygame.draw.rect(holo_surface, (AI_RED + (128,)), (0, 0, 150, 80), 2)
        lock_text = small_font.render("LOCKDOWN ACTIVE", True, WHITE)
        holo_surface.blit(lock_text, (10, 30))
        screen.blit(holo_surface, (250 + random.randint(-5, 5), 200))
        screen.blit(holo_surface, (450 + random.randint(-5, 5), 400))
    
    # Draw inter-strata portals (circles with surges)
    portal_positions = [(300, 200), (500, 400)]
    for px, py in portal_positions:
        pygame.draw.circle(screen, PORTAL_BLUE[:3], (px, py), 50, 2)
        if instability_timer % 15 < 7:  # Surge
            for _ in range(5):
                angle = random.uniform(0, 2 * math.pi)
                end_x = px + int(60 * math.cos(angle))
                end_y = py + int(60 * math.sin(angle))
                pygame.draw.line(screen, ENERGY_YELLOW, (px, py), (end_x, end_y), 2)
    
    # Draw the track: 8 turns with three tiered drops separated by flats
    track_width = 200
    start_x = (SCREEN_WIDTH - track_width) // 2
    points = []
    y_pos = 0
    drop_heights = [SCREEN_HEIGHT // 6, SCREEN_HEIGHT // 6, SCREEN_HEIGHT // 6]  # Three drops
    flat_length = SCREEN_HEIGHT // 12
    turn_count_per_section = [2, 2, 2, 2]  # Distribute 8 turns
    
    # Launch and pre-first drop: 2 turns
    section_length = (SCREEN_HEIGHT - sum(drop_heights) - 2 * flat_length) // 4  # Approx
    for turn in range(turn_count_per_section[0]):
        direction = -1 if turn % 2 == 0 else 1
        for i in range(0, section_length, 10):
            curve_x = (points[-1][0] if points else start_x + track_width // 2) + direction * int(100 * math.sin(math.pi * i / section_length))
            points.append((curve_x, y_pos))
            y_pos += 10
    
    # First drop: Steep, minimal turn
    for i in range(0, drop_heights[0], 5):
        drop_x = points[-1][0] + random.randint(-5, 5) if instability_timer % 10 < 5 else points[-1][0]
        points.append((drop_x, y_pos))
        y_pos += 10
    
    # First flat: 2 turns
    for turn in range(turn_count_per_section[1]):
        direction = 1 if turn % 2 == 0 else -1
        for i in range(0, flat_length, 10):
            curve_x = points[-1][0] + direction * int(50 * math.sin(math.pi * i / flat_length))  # Shallower turns
            points.append((curve_x, y_pos))
            y_pos += 5  # Slower descent in flat
    
    # Second drop
    for i in range(0, drop_heights[1], 5):
        drop_x = points[-1][0] + random.randint(-5, 5) if instability_timer % 10 < 5 else points[-1][0]
        points.append((drop_x, y_pos))
        y_pos += 10
    
    # Second flat: 2 turns
    for turn in range(turn_count_per_section[2]):
        direction = -1 if turn % 2 == 0 else 1
        for i in range(0, flat_length, 10):
            curve_x = points[-1][0] + direction * int(50 * math.sin(math.pi * i / flat_length))
            points.append((curve_x, y_pos))
            y_pos += 5
    
    # Third drop
    for i in range(0, drop_heights[2], 5):
        drop_x = points[-1][0] + random.randint(-5, 5) if instability_timer % 10 < 5 else points[-1][0]
        points.append((drop_x, y_pos))
        y_pos += 10
    
    # Final section: 2 turns to finish
    remaining_y = SCREEN_HEIGHT - y_pos
    for turn in range(turn_count_per_section[3]):
        direction = 1 if turn % 2 == 0 else -1
        for i in range(0, remaining_y // 2, 10):
            curve_x = points[-1][0] + direction * int(100 * math.sin(math.pi * i / (remaining_y // 2)))
            points.append((curve_x, y_pos))
            y_pos += 10
    
    # Draw the track surface
    pygame.draw.lines(screen, GLOW_GREEN, False, points, track_width)
    
    # Add gravitational buffers (soft glows at drop ends)
    drop_ends = [drop_heights[0], drop_heights[0] + flat_length + drop_heights[1], SCREEN_HEIGHT - remaining_y // 2]
    for de in drop_ends:
        if de < len(points):
            pygame.draw.circle(screen, PORTAL_BLUE[:3], points[de], 30, 5)
    
    # Draw high-altitude corporate balcony launch platform at top
    pygame.draw.rect(screen, NEON_PINK, (start_x - 50, 0, track_width + 100, 50), 5)
    
    # Text overlays for theme
    title_text = font.render("Strata Cascade Descent", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 1200m | Drop: 110m | Turns: 8 | Max Speed: 100 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Advanced tiered drops in stratified megacity layers", True, WHITE)
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
