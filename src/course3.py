import pygame
import sys
import math

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

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 3: Binary Switchback Sprawl")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

def draw_track():
    # Draw background - hazy recycled air with digital fog (gradient lines)
    screen.fill(DARK_BG)
    for y in range(0, SCREEN_HEIGHT, 5):
        alpha = int(50 * (1 - y / SCREEN_HEIGHT))
        pygame.draw.line(screen, (alpha, alpha, alpha + 20), (0, y), (SCREEN_WIDTH, y), 1)
    
    # Draw stacked hab-blocks (multiple rectangles)
    for i in range(3):
        pygame.draw.rect(screen, NEON_BLUE, (50 + i*50, 100 - i*20, 100, 400 + i*50), 2)
        pygame.draw.rect(screen, NEON_PINK, (550 - i*50, 100 - i*20, 100, 400 + i*50), 2)
    
    # Draw the track: straight start, left curve, then right curve
    track_width = 200
    start_x = (SCREEN_WIDTH - track_width) // 2
    points = []
    # Straight section
    straight_length = SCREEN_HEIGHT // 3
    for i in range(0, straight_length, 10):
        points.append((start_x + track_width // 2, i))
    
    # Left curve (shift x leftward)
    curve_length = SCREEN_HEIGHT // 3
    curve_start_y = straight_length
    for i in range(0, curve_length, 10):
        curve_x = start_x + track_width // 2 - int(150 * math.sin(math.pi * i / curve_length))
        points.append((curve_x, curve_start_y + i))
    
    # Right curve (shift x rightward)
    curve_start_y2 = straight_length + curve_length
    for i in range(0, SCREEN_HEIGHT - curve_start_y2, 10):
        curve_x = points[-1][0] + int(150 * math.sin(math.pi * i / (SCREEN_HEIGHT - curve_start_y2)))
        points.append((curve_x, curve_start_y2 + i))
    
    # Draw the track surface
    pygame.draw.lines(screen, GLOW_GREEN, False, points, track_width)
    
    # Add pulsing neural networks (lines along track)
    for point in points[::5]:
        pygame.draw.line(screen, HOLO_PURPLE, (point[0] - track_width // 2, point[1]), (point[0] + track_width // 2, point[1]), 1)
    
    # Draw mid-tier launch platform at top
    pygame.draw.rect(screen, NEON_PINK, (start_x - 50, 0, track_width + 100, 50), 5)
    
    # Binary code projections (text overlays)
    binary_text = small_font.render("01010101 10101010", True, AI_RED)
    screen.blit(binary_text, (150, 200))
    screen.blit(binary_text, (600, 300))
    
    # Drone swarms (small circles)
    for _ in range(5):
        pygame.draw.circle(screen, NEON_BLUE, (100 + _*50, 50 + _*20), 5)
        pygame.draw.circle(screen, NEON_PINK, (600 - _*50, 50 + _*20), 5)
    
    # AI graffiti (simple text)
    graffiti_text = small_font.render("Rogue AI Zone", True, AI_RED)
    screen.blit(graffiti_text, (200, 400))
    
    # Text overlays for theme
    title_text = font.render("Binary Switchback Sprawl", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 500m | Drop: 40m | Turns: 2 (left then right) | Max Speed: 65 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Novice switchbacks in dystopian mid-level districts", True, WHITE)
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
