import pygame
import sys
import math
import random  # For drone interference and vibrations

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
GRAFFITI_GRAY = (150, 150, 150)
OIL_BLACK = (20, 20, 20, 128)  # Semi-transparent for oil slicks
DRONE_ORANGE = (255, 140, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 8: Neon Chicane Underpass")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12, bold=True)

# For animation (drone interference, track vibrations, alarm flares)
interference_timer = 0

def draw_track():
    global interference_timer
    interference_timer += 1
    # Draw background - oil-slicked darkness with shadows
    screen.fill(DARK_BG)
    oil_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for y in range(0, SCREEN_HEIGHT, 20):
        pygame.draw.rect(oil_surface, OIL_BLACK, (0, y, SCREEN_WIDTH, 10))
    screen.blit(oil_surface, (0, 0))
    
    # Draw graffiti-covered pylons (vertical pillars with text)
    pylon_positions = [150, 650]
    for px in pylon_positions:
        pygame.draw.rect(screen, GRAFFITI_GRAY, (px, 0, 40, SCREEN_HEIGHT), 0)
        graffiti_text = small_font.render("Street Kings", True, AI_RED)
        screen.blit(graffiti_text, (px - 20, 150))
        graffiti_text2 = small_font.render("No Corps", True, NEON_BLUE)
        screen.blit(graffiti_text2, (px - 10, 300))
    
    # Draw elevated highways (horizontal beams overhead)
    for hy in [50, 100]:
        pygame.draw.rect(screen, NEON_PINK, (0, hy, SCREEN_WIDTH, 20), 0)
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(screen, ENERGY_YELLOW, (x, hy), (x + 25, hy + 20), 1)
    
    # Draw illicit street racer holograms (semi-transparent cars)
    holo_car_surface = pygame.Surface((80, 40), pygame.SRCALPHA)
    pygame.draw.rect(holo_car_surface, (HOLO_PURPLE + (128,)), (0, 0, 80, 40), 0)
    screen.blit(holo_car_surface, (200 + (interference_timer % 100) - 50, 200))
    screen.blit(holo_car_surface, (500 - (interference_timer % 100) + 50, 400))
    
    # Draw the track: 6 turns including tight chicane (quick zig-zag)
    track_width = 200
    start_x = (SCREEN_WIDTH - track_width) // 2
    points = []
    y_pos = 0
    section_length = SCREEN_HEIGHT // 7
    
    # Turn 1: Mild left
    for i in range(0, section_length, 10):
        curve_x = start_x + track_width // 2 - int(100 * math.sin(math.pi * i / section_length))
        points.append((curve_x, y_pos))
        y_pos += 10
    
    # Turn 2: Mild right
    for i in range(0, section_length, 10):
        curve_x = points[-1][0] + int(100 * math.sin(math.pi * i / section_length))
        points.append((curve_x, y_pos))
        y_pos += 10
    
    # Tight chicane: Quick left-right-left (turns 3-5)
    chicane_length = section_length // 2
    # Left
    for i in range(0, chicane_length, 5):
        curve_x = points[-1][0] - int(150 * math.sin(math.pi * i / chicane_length))
        points.append((curve_x + random.randint(-3, 3), y_pos))  # Vibration
        y_pos += 10
    # Right
    for i in range(0, chicane_length, 5):
        curve_x = points[-1][0] + int(150 * math.sin(math.pi * i / chicane_length))
        points.append((curve_x + random.randint(-3, 3), y_pos))
        y_pos += 10
    # Left
    for i in range(0, chicane_length, 5):
        curve_x = points[-1][0] - int(150 * math.sin(math.pi * i / chicane_length))
        points.append((curve_x + random.randint(-3, 3), y_pos))
        y_pos += 10
    
    # Turn 6: Final right to finish
    remaining_length = SCREEN_HEIGHT - y_pos
    for i in range(0, remaining_length, 10):
        curve_x = points[-1][0] + int(100 * math.sin(math.pi * i / remaining_length))
        points.append((curve_x, y_pos))
        y_pos += 10
    
    # Draw the track surface with tire marks (dashed lines)
    pygame.draw.lines(screen, GLOW_GREEN, False, points, track_width)
    for point in points[::20]:
        pygame.draw.line(screen, OIL_BLACK[:3], (point[0] - track_width // 2 + 20, point[1]), (point[0] - track_width // 2 + 60, point[1]), 5)
        pygame.draw.line(screen, OIL_BLACK[:3], (point[0] + track_width // 2 - 60, point[1]), (point[0] + track_width // 2 - 20, point[1]), 5)
    
    # Add speed sensor alarm flares (flashing at chicane)
    chicane_start_y = 2 * section_length
    if interference_timer % 20 < 10:  # Blink
        for y in range(chicane_start_y, chicane_start_y + 3 * chicane_length, 20):
            pygame.draw.circle(screen, ENERGY_YELLOW, (points[y // 10][0], y), 15)
    
    # Draw graffiti-laden overpass launch platform at top
    pygame.draw.rect(screen, NEON_PINK, (start_x - 50, 0, track_width + 100, 50), 5)
    launch_graffiti = small_font.render("Race or Die", True, AI_RED)
    screen.blit(launch_graffiti, (start_x + 20, 20))
    
    # Overhead traffic drones (moving circles with booms)
    drone_x = 300 + (interference_timer % 200) - 100
    drone_y = 80
    pygame.draw.circle(screen, DRONE_ORANGE, (drone_x, drone_y), 10)
    if interference_timer % 50 == 0:  # Sonic boom effect
        pygame.draw.circle(screen, WHITE, (drone_x, drone_y), 20, 2)
    
    # Holographic barriers in chicane (closing gaps)
    if interference_timer % 40 < 20:
        for y in range(chicane_start_y + chicane_length, chicane_start_y + 2 * chicane_length, 30):
            pygame.draw.line(screen, HOLO_PURPLE, (points[y // 10][0] - track_width // 2, y), (points[y // 10][0] + track_width // 2, y), 3)
    
    # Text overlays for theme
    title_text = font.render("Neon Chicane Underpass", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 1000m | Drop: 90m | Turns: 6 (chicane) | Max Speed: 90 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Advanced beginner chicane in shadowed highways", True, WHITE)
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
