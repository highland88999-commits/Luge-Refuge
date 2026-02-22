import pygame
import sys
import math
import random  # For consciousness imbalances, tilts, and distortions

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
NEURAL_RED = (255, 0, 0, 128)  # For synaptic overloads
MEMORY_BLUE = (0, 0, 255, 64)  # For memory shards
HALLUC_GRAY = (150, 150, 150, 128)  # For hallucinations
TILT_PURPLE = (128, 0, 128, 64)  # For visual tilts

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 18: Neural Overload Asymmetric")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# For animation (consciousness imbalances, visual tilts, uneven distortions, phantoms)
imbalance_timer = 0

def draw_track():
    global imbalance_timer
    imbalance_timer += 1
    # Draw background - skewed mind-scape with erratic synaptic overloads
    screen.fill(DARK_BG)
    # Synaptic overloads (biased to one side, more on left)
    overload_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for _ in range(10):
        ox = random.randint(50, SCREEN_WIDTH // 2) if random.random() < 0.7 else random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 50)  # Bias left
        oy = random.randint(0, SCREEN_HEIGHT)
        pygame.draw.circle(overload_surface, NEURAL_RED[:3], (ox, oy), random.randint(20, 50))
    screen.blit(overload_surface, (0, 0))
    
    # Fragmented memory shards (scattered text, biased)
    for _ in range(15):
        mx = random.randint(50, SCREEN_WIDTH // 2 + 100) if random.random() < 0.6 else random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 50)  # Left bias
        my = random.randint(50, SCREEN_HEIGHT - 50)
        shard_text = small_font.render("MEMORY SHARD", True, MEMORY_BLUE[:3])
        screen.blit(shard_text, (mx + random.randint(-5, 5), my))
    
    # Asymmetric hallucinations (one-sided, e.g., more on left)
    if imbalance_timer % 20 < 10:  # Flicker
        hall_surface = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT), pygame.SRCALPHA)  # Left side heavier
        for _ in range(8):
            hx = random.randint(0, SCREEN_WIDTH // 2)
            hy = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.rect(hall_surface, HALLUC_GRAY[:3], (hx, hy, 40, 80))
        screen.blit(hall_surface, (0, 0))
        # Minor right side
        for _ in range(3):
            hx = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH)
            hy = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.rect(screen, HALLUC_GRAY[:3], (hx, hy, 40, 80))
    
    # Persistent neural phantoms (unbalanced commands)
    phantom_positions = [(150, 150), (200, 300), (250, 450), (600, 250)]  # More left
    for px, py in phantom_positions:
        phantom_text = small_font.render("Left... Pull Left...", True, AI_RED)
        screen.blit(phantom_text, (px + random.randint(-10, 10), py))
    
    # Draw the track: 18 turns with uneven distribution (more lefts), random steep inserts
    track_width = 200
    start_x = (SCREEN_WIDTH - track_width) // 2
    points = []
    y_pos = 0
    turns = 18
    section_length = SCREEN_HEIGHT // turns
    left_turns = 12  # More lefts (biased)
    right_turns = turns - left_turns
    directions = [-1] * left_turns + [1] * right_turns
    random.shuffle(directions)  # Random but biased
    steep_inserts = random.sample(range(turns), 5)  # Random steep inserts
    
    current_x = start_x + track_width // 2
    for turn in range(turns):
        direction = directions[turn]
        is_steep = turn in steep_inserts
        radius = random.randint(80, 150) if not is_steep else 20  # Small radius for steep
        curr_length = section_length + (random.randint(20, 50) if is_steep else 0)  # Longer steep
        for i in range(0, curr_length, 5):
            curve_x = current_x + direction * int(radius * math.sin(math.pi * i / curr_length))
            tilt_offset = int(15 * math.sin(imbalance_timer / 20 + y_pos / 50)) if direction == -1 else int(5 * math.sin(imbalance_timer / 20 + y_pos / 50))  # Stronger tilt left
            distort_offset = random.randint(-10, 10) if imbalance_timer % 15 < 7 else 0  # Uneven distortion
            points.append((curve_x + tilt_offset + distort_offset, y_pos))
            y_pos += 10
        current_x = points[-1][0]
    
    # Fill to bottom
    while y_pos < SCREEN_HEIGHT:
        points.append((points[-1][0], y_pos))
        y_pos += 10
    
    # Draw the track surface
    pygame.draw.lines(screen, GLOW_GREEN, False, points, track_width)
    
    # Directional visual tilts (overlay skew, biased left)
    if imbalance_timer % 30 < 15:
        tilt_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for y in range(0, SCREEN_HEIGHT, 20):
            tilt_shift = int(20 * math.sin(imbalance_timer / 25 + y / 50))  # Tilt effect
            pygame.draw.line(tilt_surface, TILT_PURPLE[:3], (0 + tilt_shift, y), (SCREEN_WIDTH // 2 + tilt_shift, y), 2)  # Left heavier
            pygame.draw.line(tilt_surface, TILT_PURPLE[:3], (SCREEN_WIDTH // 2, y), (SCREEN_WIDTH, y), 1)  # Right lighter
        screen.blit(tilt_surface, (0, 0))
    
    # Draw asymmetric archive node launch platform at top
    pygame.draw.rect(screen, NEON_PINK, (start_x - 100, 0, track_width + 50, 50), 5)  # Skewed left
    # Biased neural fluxes (more lines left)
    for fx in range(10):
        start_side = random.choice([-150, 100]) if random.random() < 0.7 else 100  # Bias left
        f_x = start_x + start_side + random.randint(-50, 50)
        f_y = 25
        end_x = f_x + random.randint(-30, 30)
        end_y = f_y + random.randint(20, 40)
        pygame.draw.line(screen, ENERGY_YELLOW, (f_x, f_y), (end_x, end_y), 2)
    
    # Text overlays for theme
    title_text = font.render("Neural Overload Asymmetric", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 2000m | Drop: 190m | Turns: 18 (asymmetric) | Max Speed: 140 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Master asymmetry in shadow neural labyrinths", True, WHITE)
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
