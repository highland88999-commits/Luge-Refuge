import pygame
import sys
import math
import random  # For ion interference, power surges, and discharges

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
PLASMA_BLUE = (0, 191, 255, 128)  # Semi-transparent for plasma
LIGHTNING_WHITE = (255, 255, 255)
ION_CLOUD_PURPLE = (128, 0, 128, 64)  # For clouds
SPARK_ORANGE = (255, 165, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 13: Plasma Storm")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# For animation (ion interference, power surges, screen static, discharges)
surge_timer = 0

def draw_track():
    global surge_timer
    surge_timer += 1
    # Draw background - plasma-charged storm with volatile ion clouds
    screen.fill(DARK_BG)
    # Ion clouds (moving ellipses)
    cloud_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for _ in range(10):
        cx = random.randint(0, SCREEN_WIDTH) + (surge_timer % 100) - 50
        cy = random.randint(0, SCREEN_HEIGHT) + (surge_timer % 80) - 40
        pygame.draw.ellipse(cloud_surface, ION_CLOUD_PURPLE[:3], (cx, cy, 150, 80))
    screen.blit(cloud_surface, (0, 0))
    
    # Crackling lightning arcs (random lines flashing)
    if surge_timer % 15 < 5:  # Flash
        for _ in range(5):
            start_x = random.randint(100, 700)
            start_y = random.randint(0, SCREEN_HEIGHT // 2)
            for seg in range(4):
                end_x = start_x + random.randint(-50, 50)
                end_y = start_y + random.randint(20, 50)
                pygame.draw.line(screen, LIGHTNING_WHITE, (start_x, start_y), (end_x, end_y), 3)
                start_x, start_y = end_x, end_y
            # Branch
            branch_x = start_x + random.randint(-30, 30)
            branch_y = start_y + random.randint(20, 40)
            pygame.draw.line(screen, LIGHTNING_WHITE, (start_x, start_y), (branch_x, branch_y), 2)
    
    # Overloaded fusion relays (pulsing circles)
    relay_positions = [(150, 100), (650, 200), (300, 400), (500, 500)]
    for rx, ry in relay_positions:
        pulse_radius = 40 + int(10 * math.sin(surge_timer / 10))
        pygame.draw.circle(screen, ENERGY_YELLOW, (rx, ry), pulse_radius, 2)
        pygame.draw.circle(screen, AI_RED, (rx, ry), 20, 0)
    
    # Holographic storm elementals (figures hurling bolts)
    elemental_positions = [(250, 250), (550, 450)]
    for ex, ey in elemental_positions:
        # Elemental body (ellipse)
        pygame.draw.ellipse(screen, (HOLO_PURPLE + (128,)), (ex - 30, ey - 50, 60, 100), 0)
        # Bolt hurl (line to random point)
        if surge_timer % 20 < 10:
            bolt_end_x = ex + random.randint(-100, 100)
            bolt_end_y = ey + random.randint(50, 100)
            pygame.draw.line(screen, PLASMA_BLUE[:3], (ex, ey), (bolt_end_x, bolt_end_y), 4)
    
    # Draw the track: 12 turns including a 360-degree banked spiral
    track_width = 200
    center_x = SCREEN_WIDTH // 2
    points = []
    y_pos = 0
    pre_spiral_turns = 5  # Turns before spiral
    spiral_turns = 1  # Full 360 spiral
    post_spiral_turns = 6  # After
    section_length = SCREEN_HEIGHT // (pre_spiral_turns + post_spiral_turns + 3)  # Approx, extra for spiral
    
    # Pre-spiral turns
    current_x = center_x
    for turn in range(pre_spiral_turns):
        direction = -1 if turn % 2 == 0 else 1
        radius = random.randint(80, 120)
        for i in range(0, section_length, 5):
            curve_x = current_x + direction * int(radius * math.sin(math.pi * i / section_length))
            discharge_offset = random.randint(-5, 5) if surge_timer % 10 < 5 else 0  # Electrical discharge
            points.append((curve_x + discharge_offset, y_pos))
            y_pos += 10
        current_x = points[-1][0]
    
    # 360-degree banked spiral (helical downward)
    spiral_start_y = y_pos
    spiral_length = section_length * 3  # Longer for full spiral
    spiral_radius = 150
    angle_step = 2 * math.pi / (spiral_length / 10)  # Full rotation
    for i in range(0, spiral_length, 10):
        angle = i * angle_step
        spiral_x = center_x + int(spiral_radius * math.cos(angle))
        spiral_y = spiral_start_y + i
        bank_offset = int(20 * math.sin(angle))  # Banking simulation
        discharge_offset = random.randint(-10, 10) if surge_timer % 15 < 7 else 0
        points.append((spiral_x + bank_offset + discharge_offset, spiral_y))
    y_pos = points[-1][1]
    
    # Post-spiral turns
    for turn in range(post_spiral_turns):
        direction = 1 if turn % 2 == 0 else -1
        radius = random.randint(80, 120)
        for i in range(0, section_length, 5):
            curve_x = points[-1][0] + direction * int(radius * math.sin(math.pi * i / section_length))
            discharge_offset = random.randint(-5, 5) if surge_timer % 10 < 5 else 0
            points.append((curve_x + discharge_offset, y_pos))
            y_pos += 10
    
    # Fill to bottom
    while y_pos < SCREEN_HEIGHT:
        points.append((points[-1][0], y_pos))
        y_pos += 10
    
    # Draw the track surface with conductive veins (sparking lines)
    pygame.draw.lines(screen, GLOW_GREEN, False, points, track_width)
    # Veins and sparks
    for point in points[::20]:
        pygame.draw.line(screen, PLASMA_BLUE[:3], (point[0] - track_width // 2, point[1]), (point[0] + track_width // 2, point[1]), 2)
        if surge_timer % 20 < 10:  # Spark
            spark_x = point[0] + random.randint(-track_width // 2, track_width // 2)
            spark_y = point[1] + random.randint(-10, 10)
            pygame.draw.circle(screen, SPARK_ORANGE, (spark_x, spark_y), 5)
    
    # Draw storm conduit access platform at top
    pygame.draw.rect(screen, NEON_PINK, (center_x - 100, 0, 200, 50), 5)
    # Thundering relays (small pulsing rects)
    for rx in [center_x - 150, center_x + 150]:
        pygame.draw.rect(screen, ENERGY_YELLOW, (rx, 20, 40, 20), 0 if surge_timer % 10 < 5 else 2)
    
    # Simulated ion interference (screen static)
    if surge_timer % 40 < 10:  # Brief static
        static_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for _ in range(200):
            sx = random.randint(0, SCREEN_WIDTH)
            sy = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.line(static_surface, (200, 200, 200), (sx, sy), (sx + random.randint(-5, 5), sy), 1)
        screen.blit(static_surface, (0, 0))
    
    # Text overlays for theme
    title_text = font.render("Plasma Storm", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 1500m | Drop: 140m | Turns: 12 (spiral) | Max Speed: 115 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Expert spiral in plasma-charged storm conduits", True, WHITE)
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
