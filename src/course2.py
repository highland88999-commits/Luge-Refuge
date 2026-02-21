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

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 2: Holo-Curve Boulevard")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)

def draw_track():
    # Draw background - dark city night with acid rain effect (simple lines)
    screen.fill(DARK_BG)
    for y in range(0, SCREEN_HEIGHT, 10):
        pygame.draw.line(screen, (50, 50, 60), (0, y), (SCREEN_WIDTH, y + 5), 1)
    
    # Draw towering arcologies (rectangles with neon accents)
    pygame.draw.rect(screen, NEON_BLUE, (100, 50, 80, 500), 2)
    pygame.draw.rect(screen, NEON_PINK, (600, 50, 80, 500), 2)
    
    # Draw the track: straight start into a mild left curve
    # Use a bezier-like approximation for the curve
    track_width = 200
    start_x = (SCREEN_WIDTH - track_width) // 2
    points = []
    for i in range(0, SCREEN_HEIGHT // 2, 10):  # Straight section
        points.append((start_x + track_width // 2, i))
    # Curve section: mild left (shift x leftward)
    curve_start_y = SCREEN_HEIGHT // 2
    for i in range(0, SCREEN_HEIGHT // 2, 10):
        curve_x = start_x + track_width // 2 - int(100 * math.sin(math.pi * i / (SCREEN_HEIGHT // 2)))
        points.append((curve_x, curve_start_y + i))
    
    # Draw the track surface
    pygame.draw.lines(screen, GLOW_GREEN, False, points, track_width)
    
    # Add glowing data streams (lines along the track)
    for point in points[::5]:
        pygame.draw.line(screen, HOLO_PURPLE, (point[0] - track_width // 2, point[1]), (point[0] + track_width // 2, point[1]), 1)
    
    # Draw elevated walkway launch pad at top
    pygame.draw.rect(screen, NEON_PINK, (start_x - 50, 0, track_width + 100, 50), 5)
    
    # Holographic projections (semi-transparent circles)
    pygame.draw.circle(screen, (NEON_BLUE + (128,)), (200, 200), 50, 2)
    pygame.draw.circle(screen, (NEON_PINK + (128,)), (550, 300), 70, 2)
    
    # Text overlays for theme
    title_text = font.render("Holo-Curve Boulevard", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 400m | Drop: 30m | Turns: 1 (mild left) | Max Speed: 60 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Beginner curve in neon megacity underbelly", True, WHITE)
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
