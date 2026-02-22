import pygame
import sys
import math
import random  # For void entropy, gravity shifts, and illusory obstacles

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
VOID_BLACK = (0, 0, 0, 128)  # Semi-transparent for voids
ENTROPY_MIST_GRAY = (100, 100, 100, 64)  # For mist
SPECTRAL_BLUE = (0, 128, 255, 128)  # For spectral entities
ILLUSORY_GREEN = (0, 255, 0, 64)  # For illusions

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 16: Void Cascade")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# For animation (void entropy, gravity shifts, illusory obstacles, whispers)
entropy_timer = 0

def draw_track():
    global entropy_timer
    entropy_timer += 1
    # Draw background - swirling entropy mist with gravity wells
    screen.fill(DARK_BG)
    mist_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for _ in range(15):
        mx = random.randint(0, SCREEN_WIDTH) + int(50 * math.sin(entropy_timer / 20 + _))
        my = random.randint(0, SCREEN_HEIGHT) + int(30 * math.cos(entropy_timer / 20 + _))
        pygame.draw.ellipse(mist_surface, ENTROPY_MIST_GRAY[:3], (mx - 75, my - 50, 150, 100))
    screen.blit(mist_surface, (0, 0))
    
    # Distorted gravity wells (pulling circles)
    well_positions = [(200, 150), (600, 300), (400, 500)]
    for wx, wy in well_positions:
        well_radius = 60 + int(20 * math.sin(entropy_timer / 15))
        pygame.draw.circle(screen, VOID_BLACK[:3], (wx, wy), well_radius, 5)
        # Ripples
        for r in range(1, 4):
            pygame.draw.circle(screen, VOID_BLACK[:3], (wx, wy), well_radius + r * 10, 1)
    
    # Echoing void whispers (fading text)
    if entropy_timer % 25 < 12:
        whisper_text = small_font.render("Fall... Deeper...", True, SPECTRAL_BLUE[:3])
        screen.blit(whisper_text, (SCREEN_WIDTH // 2 - 100 + random.randint(-10, 10), 150))
        screen.blit(whisper_text, (SCREEN_WIDTH // 2 - 100 + random.randint(-10, 10), 450))
    
    # Spectral void entities (luring figures)
    entity_positions = [(250, 250), (550, 400)]
    for ex, ey in entity_positions:
        entity_surface = pygame.Surface((60, 120), pygame.SRCALPHA)
        pygame.draw.ellipse(entity_surface, SPECTRAL_BLUE[:3], (0, 0, 60, 120))
        shift_x = ex + int(15 * math.sin(entropy_timer / 20))
        shift_y = ey + int(10 * math.cos(entropy_timer / 20))
        screen.blit(entity_surface, (shift_x, shift_y))
        # Lure lines to traps
        if entropy_timer % 30 < 15:
            trap_x = shift_x + random.randint(-100, 100)
            trap_y = shift_y + random.randint(50, 100)
            pygame.draw.line(screen, AI_RED, (shift_x + 30, shift_y + 60), (trap_x, trap_y), 2)
    
    # Draw the track: 16 turns with chicanes, drops, banks; path fracturing
    track_width = 200
    start_x = (SCREEN_WIDTH - track_width) // 2
    points = []
    y_pos = 0
    turns = 16
    section_length = SCREEN_HEIGHT // turns
    # Alternate elements: chicane (quick turns), drop (steep), bank (curved)
    patterns = ['chicane', 'drop', 'bank'] * (turns // 3) + ['chicane', 'drop']  # Mix
    
    current_x = start_x + track_width // 2
    for turn in range(turns):
        pattern = patterns[turn % len(patterns)]
        direction = -1 if turn % 2 == 0 else 1
        radius = random.randint(100, 150)
        
        if pattern == 'chicane':
            # Quick zig-zag
            chicane_sub = section_length // 3
            for sub in range(3):
                sub_dir = direction * (-1 if sub % 2 else 1)
                for i in range(0, chicane_sub, 5):
                    curve_x = current_x + sub_dir * int(120 * math.sin(math.pi * i / chicane_sub))
                    points.append((curve_x, y_pos))
                    y_pos += 10
        elif pattern == 'drop':
            # Steep drop
            for i in range(0, section_length, 3):
                drop_x = current_x + random.randint(-10, 10)  # Wobble
                points.append((drop_x, y_pos))
                y_pos += 10
        else:  # Bank
            # Curved bank
            for i in range(0, section_length, 5):
                curve_x = current_x + direction * int(radius * math.sin(math.pi * i / section_length))
                bank_offset = int(20 * math.cos(math.pi * i / section_length))  # Banking
                points.append((curve_x + bank_offset, y_pos))
                y_pos += 10
        
        if points:
            current_x = points[-1][0]
    
    # Fill to bottom
    while y_pos < SCREEN_HEIGHT:
        points.append((points[-1][0], y_pos))
        y_pos += 10
    
    # Draw the track with fracturing (multi-path illusions)
    pygame.draw.lines(screen, GLOW_GREEN, False, points, track_width)
    if entropy_timer % 30 < 15:  # Fracture
        fracture_start = random.randint(50, len(points) - 50)
        fracture_points = [(p[0] + random.randint(-50, 50), p[1]) for p in points[fracture_start:fracture_start + 50]]
        pygame.draw.lines(screen, ILLUSORY_GREEN[:3], False, fracture_points, track_width // 2)
        # Converge back
        converge_point = points[fracture_start + 50]
        pygame.draw.line(screen, ILLUSORY_GREEN[:3], fracture_points[-1], converge_point, track_width // 2)
    
    # Cascade stabilizers (glowing points reforming track)
    for sy in range(100, SCREEN_HEIGHT, 150):
        pygame.draw.circle(screen, ENERGY_YELLOW, points[sy // 10], 20, 2)
    
    # Simulated void entropy gravity shifts (track warp)
    if entropy_timer % 40 < 10:
        for i in range(len(points)):
            points[i] = (points[i][0] + random.randint(-5, 5), points[i][1])
    
    # Illusory obstacles (random blocks)
    if entropy_timer % 25 < 12:
        for _ in range(3):
            ox = random.randint(100, 700)
            oy = random.randint(100, 500)
            pygame.draw.rect(screen, AI_RED, (ox, oy, 50, 50), 0)
    
    # Draw cascade gateway launch platform at top
    pygame.draw.rect(screen, NEON_PINK, (start_x - 50, 0, track_width + 100, 50), 5)
    # Rippling entropy waves (lines from platform)
    for wx in range(start_x, start_x + track_width, 20):
        wave_y = 50 + int(10 * math.sin(entropy_timer / 10 + wx / 20))
        pygame.draw.line(screen, ENTROPY_MIST_GRAY[:3], (wx, 50), (wx, wave_y), 3)
    
    # Text overlays for theme
    title_text = font.render("Void Cascade", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 1800m | Drop: 170m | Turns: 16 | Max Speed: 130 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Elite combo in subspace voids cascade", True, WHITE)
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
