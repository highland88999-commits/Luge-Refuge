import pygame
import sys
import math
import random  # For barrier collapses, reality warps, and adaptive fusions

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
RIFT_COLLAPSE_BLACK = (0, 0, 0, 128)  # For collapses
STORM_PURPLE = (128, 0, 128, 64)  # For storms
ANOMALY_ORANGE = (255, 165, 0, 128)  # For hybrid anomalies
OVERLORD_RED = (255, 0, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 20: Quantum Rift Ultimatum")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# For animation (barrier collapses, reality warps, overlord interventions, multi-realm distortions)
collapse_timer = 0

def draw_track():
    global collapse_timer
    collapse_timer += 1
    # Draw background - collapsing quantum maelstrom with converging storms
    screen.fill(DARK_BG)
    # Rift collapses (expanding black holes)
    collapse_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for _ in range(4):
        cx = random.randint(100, 700)
        cy = random.randint(100, 500)
        radius = 30 + int(20 * math.sin(collapse_timer / 15 + _))
        pygame.draw.circle(collapse_surface, RIFT_COLLAPSE_BLACK[:3], (cx, cy), radius)
    screen.blit(collapse_surface, (0, 0))
    
    # Converging reality storms (swirling mists from multiple realms)
    storm_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for _ in range(10):
        sx = SCREEN_WIDTH // 2 + int(150 * math.cos(collapse_timer / 20 + _ * math.pi / 5))
        sy = SCREEN_HEIGHT // 2 + int(100 * math.sin(collapse_timer / 20 + _ * math.pi / 5))
        pygame.draw.ellipse(storm_surface, STORM_PURPLE[:3], (sx - 50, sy - 30, 100, 60))
    screen.blit(storm_surface, (0, 0))
    
    # Hybrid anomalies (fused from prior: wind + plasma + neural, etc.)
    if collapse_timer % 20 < 10:  # Anomalous flashes
        for _ in range(8):
            ax = random.randint(50, SCREEN_WIDTH - 50)
            ay = random.randint(50, SCREEN_HEIGHT - 50)
            pygame.draw.circle(screen, ANOMALY_ORANGE[:3], (ax, ay), random.randint(20, 40))
            # Wind lines
            pygame.draw.line(screen, NEON_BLUE, (ax, ay), (ax + random.randint(-40, 40), ay), 2)
            # Plasma spark
            pygame.draw.line(screen, ENERGY_YELLOW, (ax, ay), (ax, ay + random.randint(-30, 30)), 3)
    
    # Omnipresent rift overlords (large fused titans intervening)
    overlord_positions = [(SCREEN_WIDTH // 2, 200 + math.sin(collapse_timer / 10) * 20), (SCREEN_WIDTH // 2, 400 + math.cos(collapse_timer / 10) * 20)]
    for ox, oy in overlord_positions:
        pygame.draw.ellipse(screen, OVERLORD_RED, (ox - 100, oy - 150, 200, 300), 5)
        if collapse_timer % 30 < 15:  # Assault beams
            beam_end_x = ox + random.randint(-200, 200)
            beam_end_y = oy + random.randint(100, 200)
            pygame.draw.line(screen, AI_RED, (ox, oy), (beam_end_x, beam_end_y), 5)
    
    # Draw the track: 20 turns integrating spirals, plunges, chicanes, narrow paths, wind, asymmetric
    track_width = 200
    start_x = (SCREEN_WIDTH - track_width) // 2
    points = []
    y_pos = 0
    turns = 20
    section_length = SCREEN_HEIGHT // turns
    # Feature mix: spiral (long curve), plunge (steep), chicane (zigzag), narrow (width/2), wind (sway), asymmetric (biased dir)
    features = random.sample(['spiral', 'plunge', 'chicane', 'narrow', 'wind', 'asymmetric'] * 4, turns)  # Mixed
    
    current_x = start_x + track_width // 2
    direction_bias = -1  # Asymmetric bias to left
    for turn in range(turns):
        feature = features[turn]
        direction = direction_bias if random.random() < 0.7 else -direction_bias  # Biased
        radius = random.randint(80, 150)
        curr_width = track_width // 2 if feature == 'narrow' else track_width
        curr_length = section_length
        
        if feature == 'spiral':
            angle_step = 2 * math.pi / (curr_length / 5)
            for i in range(0, curr_length, 5):
                angle = i * angle_step
                spiral_x = current_x + int(radius * math.cos(angle))
                spiral_y = y_pos + i
                points.append((spiral_x, spiral_y))
                y_pos += 10
        elif feature == 'plunge':
            curr_length *= 1.5  # Longer plunge
            for i in range(0, curr_length, 3):
                plunge_x = current_x + random.randint(-10, 10)
                points.append((plunge_x, y_pos))
                y_pos += 10
        elif feature == 'chicane':
            chicane_sub = curr_length // 3
            for sub in range(3):
                sub_dir = direction * (-1 if sub % 2 else 1)
                for i in range(0, chicane_sub, 5):
                    curve_x = current_x + sub_dir * int(120 * math.sin(math.pi * i / chicane_sub))
                    points.append((curve_x, y_pos))
                    y_pos += 10
        elif feature == 'narrow':
            for i in range(0, curr_length, 5):
                curve_x = current_x + direction * int(radius * math.sin(math.pi * i / curr_length))
                points.append((curve_x, y_pos))
                y_pos += 10
        elif feature == 'wind':
            for i in range(0, curr_length, 5):
                curve_x = current_x + direction * int(radius * math.sin(math.pi * i / curr_length))
                wind_sway = int(15 * math.sin(collapse_timer / 15 + y_pos / 50))
                points.append((curve_x + wind_sway, y_pos))
                y_pos += 10
        else:  # Asymmetric
            for i in range(0, curr_length, 5):
                curve_x = current_x + direction * int(radius * math.sin(math.pi * i / curr_length))
                asym_offset = random.randint(-20, 5) if direction == -1 else random.randint(-5, 20)  # Biased offset
                points.append((curve_x + asym_offset, y_pos))
                y_pos += 10
        
        if points:
            current_x = points[-1][0]
    
    # Fill to bottom
    while y_pos < SCREEN_HEIGHT:
        points.append((points[-1][0], y_pos))
        y_pos += 10
    
    # Draw the track with disintegrating effects (fading segments)
    for seg in range(0, len(points), 50):
        seg_points = points[seg:seg+50]
        alpha = 255 if collapse_timer % 40 < 20 else 128  # Disintegrate fade
        track_color = (GLOW_GREEN[0], GLOW_GREEN[1], GLOW_GREEN[2], alpha)
        pygame.draw.lines(screen, track_color[:3], False, seg_points, track_width)
    
    # Multi-realm distortions (hybrid from prior: echoes + warps + sparks)
    if collapse_timer % 25 < 12:
        distort_points = [(p[0] + random.randint(-20, 20), p[1]) for p in points[::20]]
        pygame.draw.lines(screen, ANOMALY_ORANGE[:3], False, distort_points, track_width // 2)
        # Sparks
        for p in distort_points:
            pygame.draw.circle(screen, ENERGY_YELLOW, p, 5)
    
    # Draw multiversal breach launch platform at top
    pygame.draw.rect(screen, NEON_PINK, (start_x - 50, 0, track_width + 100, 50), 5)
    # Shattering converging fluxes (random lines converging to center)
    for _ in range(15):
        fx = random.randint(0, SCREEN_WIDTH)
        fy = random.randint(0, 50)
        end_x = start_x + track_width // 2 + random.randint(-50, 50)
        end_y = 50 + random.randint(20, 40)
        pygame.draw.line(screen, ENERGY_YELLOW, (fx, fy), (end_x, end_y), 2)
    
    # Text overlays for theme
    title_text = font.render("Quantum Rift Ultimatum", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 2200m | Drop: 210m | Turns: 20 | Max Speed: 150 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Master gauntlet in fracturing quantum rift", True, WHITE)
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
