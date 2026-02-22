import pygame
import sys
import math
import random  # For probability drains, screen fades, and echoes

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
RIFT_VOID = (5, 5, 15, 128)  # Semi-transparent for void horizons
ECHO_GRAY = (150, 150, 150, 64)  # For probability echoes
ENTANGLE_FIELD_PURPLE = (128, 0, 128, 64)  # For lingering fields
AFTERIMAGE_BLUE = (0, 128, 255, 32)  # For afterimages

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 17: Quantum Rift Endurance")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# For animation (probability drains, screen fades, lingering distortions, whispers)
drain_timer = 0

def draw_track():
    global drain_timer
    drain_timer += 1
    # Draw background - vast echoing void with subspace horizons
    screen.fill(DARK_BG)
    # Horizon rifts (horizontal gradients)
    for y in range(0, SCREEN_HEIGHT, 100):
        rift_surface = pygame.Surface((SCREEN_WIDTH, 50), pygame.SRCALPHA)
        rift_surface.fill(RIFT_VOID[:3])
        screen.blit(rift_surface, (0, y + int(20 * math.sin(drain_timer / 20 + y / 50))))
    
    # Persistent probability echoes (fading duplicates of elements)
    echo_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    if drain_timer % 25 < 12:  # Echo flicker
        for _ in range(5):
            ex = random.randint(100, 700)
            ey = random.randint(100, 500)
            pygame.draw.rect(echo_surface, ECHO_GRAY[:3], (ex, ey, 100, 50), 2)
    screen.blit(echo_surface, (random.randint(-5, 5), random.randint(-5, 5)))  # Slight shift
    
    # Lingering entanglement fields (web-like lines draining focus)
    field_nodes = [(100, 100), (700, 150), (200, 350), (600, 400), (300, 550)]
    for i in range(len(field_nodes)):
        for j in range(i + 1, len(field_nodes)):
            alpha = 64 + int(32 * math.sin(drain_timer / 30 + i + j))
            color = (ENTANGLE_FIELD_PURPLE[0], ENTANGLE_FIELD_PURPLE[1], ENTANGLE_FIELD_PURPLE[2], alpha)
            pygame.draw.line(screen, color[:3], field_nodes[i], field_nodes[j], 1)
    
    # Quantum afterimages (faint track ghosts)
    afterimage_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    # (We'll add track points later and echo them)
    
    # Whispering rift anomalies (text in void)
    if drain_timer % 30 < 15:
        anomaly_text = small_font.render("Endure... Fade...", True, AI_RED)
        screen.blit(anomaly_text, (SCREEN_WIDTH // 2 - 80 + random.randint(-10, 10), 200))
        screen.blit(anomaly_text, (SCREEN_WIDTH // 2 - 80 + random.randint(-10, 10), 400))
    
    # Draw the track: 17 turns with extended flats after drops
    track_width = 200
    start_x = (SCREEN_WIDTH - track_width) // 2
    points = []
    y_pos = 0
    turns = 17
    section_length = SCREEN_HEIGHT // turns
    drop_intervals = [3, 7, 11, 15]  # Drops after these turns
    flat_extra = section_length // 2  # Extra length for flats
    
    current_x = start_x + track_width // 2
    for turn in range(turns):
        is_drop = turn in drop_intervals
        is_flat = turn - 1 in drop_intervals  # Flat after drop
        direction = -1 if turn % 2 == 0 else 1
        radius = random.randint(80, 140) if not is_drop and not is_flat else 20  # Minimal curve for drop/flat
        
        curr_length = section_length + (flat_extra if is_flat else 0)
        for i in range(0, curr_length, 5 if not is_drop else 3):  # Faster in drop
            if is_drop:
                curve_x = current_x + random.randint(-10, 10)  # Wobble in drop
            else:
                curve_x = current_x + direction * int(radius * math.sin(math.pi * i / curr_length))
            drain_offset = random.randint(-8, 8) if drain_timer % 20 < 10 else 0  # Drain shake
            points.append((curve_x + drain_offset, y_pos))
            y_pos += 10
        current_x = points[-1][0]
    
    # Fill to bottom
    while y_pos < SCREEN_HEIGHT:
        points.append((points[-1][0], y_pos))
        y_pos += 10
    
    # Draw the track surface
    pygame.draw.lines(screen, GLOW_GREEN, False, points, track_width)
    
    # Rift-induced echoes (lingering distortions of track)
    echo_points = [(p[0] + random.randint(-20, 20), p[1] + random.randint(0, 10)) for p in points[::10]]
    pygame.draw.lines(afterimage_surface, AFTERIMAGE_BLUE[:3], False, echo_points, track_width // 2)
    screen.blit(afterimage_surface, (0, 0))
    
    # Simulated probability drains (gradual screen fades)
    fade_alpha = min(128, drain_timer % 100)  # Build up fade
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    fade_surface.fill((0, 0, 0, fade_alpha // 2))  # Darken
    screen.blit(fade_surface, (0, 0))
    
    # Draw horizon rift stabilizer platform at top
    pygame.draw.rect(screen, NEON_PINK, (start_x - 50, 0, track_width + 100, 50), 5)
    # Vibrating infinite echoes (duplicated platforms faint)
    for e in range(1, 3):
        echo_alpha = 128 // e
        echo_surface = pygame.Surface((track_width + 100, 50), pygame.SRCALPHA)
        pygame.draw.rect(echo_surface, (NEON_PINK[0], NEON_PINK[1], NEON_PINK[2], echo_alpha), (0, 0, track_width + 100, 50), 5)
        screen.blit(echo_surface, (start_x - 50 + random.randint(-5 * e, 5 * e), 50 * e))
    
    # Text overlays for theme
    title_text = font.render("Quantum Rift Endurance", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 1900m | Drop: 180m | Turns: 17 | Max Speed: 135 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Elite endurance in expansive quantum rifts", True, WHITE)
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
