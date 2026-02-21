import pygame
import sys
import math
import random  # For electromagnetic pulses simulation

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
LASER_ORANGE = (255, 165, 0)
MIST_GRAY = (100, 100, 100, 64)  # Semi-transparent for mist

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 5: Synth-Serpentine Nexus")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# For animation (electromagnetic pulses and glitches)
pulse_timer = 0

def draw_track():
    global pulse_timer
    pulse_timer += 1
    # Draw background - encrypted mist haze (semi-transparent overlay)
    screen.fill(DARK_BG)
    mist_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    mist_surface.fill(MIST_GRAY)
    screen.blit(mist_surface, (0, 0))
    
    # Draw interconnected data nexuses (nodes as circles connected by lines)
    pygame.draw.circle(screen, NEON_BLUE, (200, 150), 30, 2)
    pygame.draw.circle(screen, NEON_PINK, (600, 250), 40, 2)
    pygame.draw.circle(screen, HOLO_PURPLE, (300, 400), 35, 2)
    pygame.draw.line(screen, AI_RED, (200, 150), (600, 250), 1)
    pygame.draw.line(screen, AI_RED, (600, 250), (300, 400), 1)
    
    # Draw streaming code waterfalls (vertical lines with text)
    for x in [100, 700]:
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(screen, ENERGY_YELLOW, (x, y), (x, y + 40), 2)
            code_text = small_font.render("101010", True, ENERGY_YELLOW)
            screen.blit(code_text, (x - 20, y + 10))
    
    # Draw augmented billboards (rects with text)
    pygame.draw.rect(screen, NEON_BLUE, (150, 200, 100, 50), 2)
    bill_text = small_font.render("Live Hack Feed", True, WHITE)
    screen.blit(bill_text, (155, 215))
    pygame.draw.rect(screen, NEON_PINK, (550, 300, 100, 50), 2)
    bill_text2 = small_font.render("Quantum Alert", True, WHITE)
    screen.blit(bill_text2, (555, 315))
    
    # Draw the track: S-shaped sequence (e.g., right curve, left curve, right curve)
    track_width = 200
    start_x = (SCREEN_WIDTH - track_width) // 2
    points = []
    
    # Short straight intro
    intro_length = SCREEN_HEIGHT // 10
    for i in range(0, intro_length, 10):
        points.append((start_x + track_width // 2, i))
    
    # First right curve (shift x rightward)
    curve_length = SCREEN_HEIGHT // 4
    curve_start_y = intro_length
    for i in range(0, curve_length, 10):
        curve_x = points[-1][0] + int(150 * math.sin(math.pi * i / curve_length))
        points.append((curve_x, curve_start_y + i))
    
    # Second left curve (shift x leftward)
    curve_start_y2 = curve_start_y + curve_length
    for i in range(0, curve_length, 10):
        curve_x = points[-1][0] - int(150 * math.sin(math.pi * i / curve_length))
        points.append((curve_x, curve_start_y2 + i))
    
    # Third right curve (shift x rightward)
    curve_start_y3 = curve_start_y2 + curve_length
    remaining_length = SCREEN_HEIGHT - curve_start_y3
    for i in range(0, remaining_length, 10):
        curve_x = points[-1][0] + int(150 * math.sin(math.pi * i / remaining_length))
        points.append((curve_x, curve_start_y3 + i))
    
    # Draw the track surface with low banking (simple lines)
    pygame.draw.lines(screen, GLOW_GREEN, False, points, track_width)
    
    # Add quantum processor pulses (flashing along track)
    if pulse_timer % 30 < 15:  # Blink effect
        for point in points[::10]:
            offset = random.randint(-10, 10) if pulse_timer % 5 == 0 else 0  # Distortion
            pygame.draw.circle(screen, ENERGY_YELLOW, (point[0] + offset, point[1]), 5)
    
    # Draw central data hub launch platform at top
    pygame.draw.rect(screen, NEON_PINK, (start_x - 50, 0, track_width + 100, 50), 5)
    pygame.draw.line(screen, HOLO_PURPLE, (start_x, 25), (start_x - 100, 25), 2)  # Fiber-optic cables
    pygame.draw.line(screen, HOLO_PURPLE, (start_x + track_width, 25), (start_x + track_width + 100, 25), 2)
    
    # Phantom drones (small triangles)
    drone_points = [(250, 100), (260, 80), (270, 100)]
    pygame.draw.polygon(screen, LASER_ORANGE, drone_points)
    drone_points2 = [(500, 200), (510, 180), (520, 200)]
    pygame.draw.polygon(screen, LASER_ORANGE, drone_points2)
    
    # Laser grids (crossing lines)
    for y in [150, 350, 500]:
        pygame.draw.line(screen, LASER_ORANGE, (100, y), (700, y), 1)
    
    # Text overlays for theme
    title_text = font.render("Synth-Serpentine Nexus", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 700m | Drop: 60m | Turns: 3 (S-shaped) | Max Speed: 75 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Intermediate S-curves in neural grid heart", True, WHITE)
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
