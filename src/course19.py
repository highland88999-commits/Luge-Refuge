import pygame
import sys
import math
import random  # For entropy distortions, time-slow, and warps

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
ENTROPY_BLACK = (0, 0, 0, 128)  # Semi-transparent for vortices
CHAOS_RED = (255, 0, 0, 64)  # For chaos crystals
VOID_SLICK_BLUE = (0, 0, 255, 32)  # For slick voids
GUARDIAN_PURPLE = (128, 0, 128, 128)  # For guardians

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 19: Entropy Cascade")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# For animation (entropy distortions, time-slow effects, visual warps, guardians)
distortion_timer = 0

def draw_track():
    global distortion_timer
    distortion_timer += 1
    # Draw background - unraveling entropy storm with swirling vortices
    screen.fill(DARK_BG)
    vortex_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for _ in range(6):
        vx = SCREEN_WIDTH // 2 + int(200 * math.cos(distortion_timer / 20 + _ * math.pi / 3))
        vy = SCREEN_HEIGHT // 2 + int(150 * math.sin(distortion_timer / 20 + _ * math.pi / 3))
        pygame.draw.circle(vortex_surface, ENTROPY_BLACK[:3], (vx, vy), random.randint(50, 100))
    screen.blit(vortex_surface, (0, 0))
    
    # Fracturing dimension shards (sharp polygons)
    if distortion_timer % 15 < 7:  # Flash
        for _ in range(10):
            sx = random.randint(50, SCREEN_WIDTH - 50)
            sy = random.randint(50, SCREEN_HEIGHT - 50)
            shard_points = [(sx, sy), (sx + random.randint(20, 50), sy - random.randint(20, 50)),
                            (sx + random.randint(50, 80), sy), (sx + random.randint(20, 50), sy + random.randint(20, 50))]
            pygame.draw.polygon(screen, CHAOS_RED[:3], shard_points)
    
    # Holographic entropy guardians (leaping traps)
    guardian_positions = [(200 + (distortion_timer % 200) - 100, 150), (600 - (distortion_timer % 200) + 100, 350), (400, 500 + math.sin(distortion_timer / 10) * 20)]
    for gx, gy in guardian_positions:
        pygame.draw.ellipse(screen, GUARDIAN_PURPLE[:3], (gx - 30, gy - 50, 60, 100))
        if distortion_timer % 30 < 15:  # Leap animation
            leap_x = gx + random.randint(-50, 50)
            leap_y = gy + random.randint(-30, 0)
            pygame.draw.line(screen, AI_RED, (gx, gy), (leap_x, leap_y), 3)
    
    # Draw the track: 19 turns with jumps, variable textures
    track_width = 200
    start_x = (SCREEN_WIDTH - track_width) // 2
    points = []
    y_pos = 0
    turns = 19
    section_length = SCREEN_HEIGHT // turns
    jump_intervals = random.sample(range(turns), 5)  # Random jumps
    texture_types = random.choices(['slick', 'standard', 'jagged'], weights=[0.4, 0.3, 0.3], k=turns)  # Variable textures
    
    current_x = start_x + track_width // 2
    for turn in range(turns):
        is_jump = turn in jump_intervals
        direction = -1 if turn % 2 == 0 else 1
        radius = random.randint(80, 150)
        curr_length = section_length
        if is_jump:
            curr_length //= 2  # Shorter ramp-up to jump
        
        for i in range(0, curr_length, 5):
            curve_x = current_x + direction * int(radius * math.sin(math.pi * i / curr_length))
            warp_offset = random.randint(-15, 15) if distortion_timer % 20 < 10 else 0  # Path shift
            points.append((curve_x + warp_offset, y_pos))
            y_pos += 10
        
        if is_jump:
            # Air gap: skip vertical, simulate jump
            air_height = random.randint(20, 40)  # Pixels for air
            land_x = points[-1][0] + random.randint(-20, 20)  # Landing variance
            y_pos += air_height
            points.append((land_x, y_pos - 10))  # Connect post-jump
        
        current_x = points[-1][0]
    
    # Fill to bottom
    while y_pos < SCREEN_HEIGHT:
        points.append((points[-1][0], y_pos))
        y_pos += 10
    
    # Draw the track surface with variable textures
    pygame.draw.lines(screen, GLOW_GREEN, False, points, track_width)
    texture_start = 0
    for t in range(turns):
        texture = texture_types[t]
        tex_length = section_length
        for i in range(texture_start, texture_start + tex_length, 10):
            if i < len(points):
                color = VOID_SLICK_BLUE[:3] if texture == 'slick' else CHAOS_RED[:3] if texture == 'jagged' else GLOW_GREEN
                pygame.draw.line(screen, color, (points[i][0] - track_width // 2, points[i][1]), (points[i][0] + track_width // 2, points[i][1]), 5 if texture == 'jagged' else 2)
        texture_start += tex_length
    
    # Simulated dimension fractures (brief time-slow visual, warps)
    if distortion_timer % 40 < 10:  # Time-slow effect (darker overlay)
        slow_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        slow_surface.fill((0, 0, 0, 64))
        screen.blit(slow_surface, (0, 0))
        # Warp points temporarily
        for i in range(len(points)):
            points[i] = (points[i][0] + random.randint(-10, 10), points[i][1])
    
    # Draw entropy nexus launch platform at top
    pygame.draw.rect(screen, NEON_PINK, (start_x - 50, 0, track_width + 100, 50), 5)
    # Crumbling chaotic fluxes (random shards around platform)
    for _ in range(10):
        fx = start_x + random.randint(-100, track_width + 100)
        fy = random.randint(0, 50)
        shard_points = [(fx, fy), (fx + 10, fy - 10), (fx + 20, fy), (fx + 10, fy + 10)]
        pygame.draw.polygon(screen, CHAOS_RED[:3], shard_points)
    
    # Text overlays for theme
    title_text = font.render("Entropy Cascade", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 2100m | Drop: 200m | Turns: 19 | Max Speed: 145 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Master jumps in chaotic entropy cascades", True, WHITE)
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
