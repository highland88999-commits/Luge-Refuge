import pygame
import sys
import math
import random  # For quantum interference, track morphing, and echoes

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
RIFT_BLUE = (0, 128, 255, 128)  # Semi-transparent for rifts
PROB_FIELD_GREEN = (0, 255, 0, 64)  # For probability fields
ENTANGLE_WEB_PURPLE = (128, 0, 128)
ECHO_GRAY = (200, 200, 200, 64)  # For visual echoes

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 14: Quantum Rift Gauntlet")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# For animation (quantum interference, track morphing, visual echoes, anomalies)
interference_timer = 0

def draw_track():
    global interference_timer
    interference_timer += 1
    # Draw background - unstable quantum rifts with subspace haze
    screen.fill(DARK_BG)
    # Rift voids (large semi-transparent areas)
    rift_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for _ in range(5):
        rx = random.randint(0, SCREEN_WIDTH) + (interference_timer % 50) - 25
        ry = random.randint(0, SCREEN_HEIGHT) + (interference_timer % 40) - 20
        pygame.draw.ellipse(rift_surface, RIFT_BLUE[:3], (rx, ry, 200, 100))
    screen.blit(rift_surface, (0, 0))
    
    # Fluctuating probability fields (wavy lines)
    for y in range(0, SCREEN_HEIGHT, 20):
        wave_offset = int(30 * math.sin(interference_timer / 15 + y / 50))
        pygame.draw.line(screen, PROB_FIELD_GREEN[:3], (100 + wave_offset, y), (700 + wave_offset, y), 2)
    
    # Shimmering entanglement webs (connected lines/nodes)
    web_nodes = [(150, 100), (650, 150), (300, 300), (500, 400), (200, 500)]
    for i in range(len(web_nodes)):
        for j in range(i + 1, len(web_nodes)):
            if random.random() > 0.5 or interference_timer % 20 < 10:  # Shimmer
                pygame.draw.line(screen, ENTANGLE_WEB_PURPLE, web_nodes[i], web_nodes[j], 1)
    
    # Quantum guardians (patrolling holograms emitting pulses)
    guardian_positions = [(200 + (interference_timer % 300) - 150, 200), (600 - (interference_timer % 300) + 150, 400)]
    for gx, gy in guardian_positions:
        pygame.draw.circle(screen, AI_RED, (gx, gy), 30, 2)
        if interference_timer % 25 < 12:  # Pulse
            pygame.draw.circle(screen, HOLO_PURPLE, (gx, gy), 50 + random.randint(0, 10), 1)
    
    # Draw the track: 13 turns with alternating wide/narrow sections, phasing
    base_track_width = 200
    points = []
    y_pos = 0
    turn_lengths = [SCREEN_HEIGHT // 14] * 13  # Approx for 13 turns
    widths = [base_track_width if i % 2 == 0 else base_track_width // 2 for i in range(13)]  # Alternate wide/narrow
    
    current_x = SCREEN_WIDTH // 2
    for turn in range(13):
        direction = -1 if turn % 2 == 0 else 1
        section_length = turn_lengths[turn]
        radius = random.randint(80, 150)
        track_width = widths[turn]
        for i in range(0, section_length, 5):
            curve_x = current_x + direction * int(radius * math.sin(math.pi * i / section_length))
            morph_offset = random.randint(-10, 10) if interference_timer % 15 < 7 else 0  # Track morphing
            points.append((curve_x + morph_offset, y_pos))
            y_pos += 10
        current_x = points[-1][0]
    
    # Fill to bottom if needed
    while y_pos < SCREEN_HEIGHT:
        points.append((points[-1][0], y_pos))
        y_pos += 10
    
    # Draw the track surface with phasing (fading in/out)
    alpha = 255 if interference_timer % 30 < 15 else 128  # Phasing
    track_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    pygame.draw.lines(track_surface, GLOW_GREEN + (alpha,), False, points, base_track_width)  # Use base for drawing, but vary logically
    screen.blit(track_surface, (0, 0))
    
    # Narrow sections visual (barriers in narrow parts)
    narrow_y_starts = [sum(turn_lengths[:turn]) for turn in range(1, 13, 2)]  # Every odd section narrow
    for ny in narrow_y_starts:
        for i in range(ny, ny + turn_lengths[0], 20):
            if i < len(points):
                px = points[i][0]
                pygame.draw.line(screen, NEON_PINK, (px - base_track_width // 4, i), (px - base_track_width // 4 - 20, i), 3)
                pygame.draw.line(screen, NEON_PINK, (px + base_track_width // 4, i), (px + base_track_width // 4 + 20, i), 3)
    
    # Random anomaly events (distortions)
    if interference_timer % 40 < 10:
        anomaly_y = random.randint(100, SCREEN_HEIGHT - 100)
        pygame.draw.circle(screen, ENERGY_YELLOW, points[anomaly_y // 10], 50, 5)
    
    # Visual echoes (faint duplicates of track segments)
    if interference_timer % 25 < 12:
        echo_points = [ (p[0] + random.randint(-20, 20), p[1] + random.randint(-5, 5)) for p in points[::10] ]
        pygame.draw.lines(screen, ECHO_GRAY[:3], False, echo_points, base_track_width // 2)
    
    # Draw rift portal launch platform at top
    pygame.draw.rect(screen, NEON_PINK, (SCREEN_WIDTH // 2 - 100, 0, 200, 50), 5)
    # Probability fluxes (random lines around platform)
    for _ in range(10):
        fx = SCREEN_WIDTH // 2 + random.randint(-150, 150)
        fy = 25 + random.randint(-20, 20)
        end_x = fx + random.randint(-30, 30)
        end_y = fy + random.randint(-30, 30)
        pygame.draw.line(screen, PROB_FIELD_GREEN[:3], (fx, fy), (end_x, end_y), 2)
    
    # Text overlays for theme
    title_text = font.render("Quantum Rift Gauntlet", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 1600m | Drop: 150m | Turns: 13 | Max Speed: 120 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Expert gauntlet in unstable quantum rifts", True, WHITE)
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
