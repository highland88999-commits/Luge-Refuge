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
METALLIC_GRAY = (169, 169, 169)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Bobsled: Generic 1 - Standard Racer")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 100  # Pixels for visualization
SLED_WIDTH = 40
SLED_COLOR = METALLIC_GRAY
ACCENT_COLOR = NEON_BLUE

# Simple track simulation for auto-call (straight path with curves)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(100 * math.sin(math.pi * i / SCREEN_HEIGHT))
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Draw chassis
    sled_rect = pygame.Rect(pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2, SLED_LENGTH, SLED_WIDTH)
    pygame.draw.rect(screen, SLED_COLOR, sled_rect)
    # Neon accents
    pygame.draw.line(screen, ACCENT_COLOR, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2), (pos_x + SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2), 3)
    pygame.draw.line(screen, ACCENT_COLOR, (pos_x - SLED_LENGTH // 2, pos_y + SLED_WIDTH // 2), (pos_x + SLED_LENGTH // 2, pos_y + SLED_WIDTH // 2), 3)
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 10, pos_y + offset, SLED_LENGTH - 20, 5))

def draw_scene():
    screen.fill(DARK_BG)
    # Draw simple track for context
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track (follow points)
    sled_index = (pygame.time.get_ticks() // 20) % len(track_points)  # Animate along track
    sled_x, sled_y = track_points[sled_index]
    # Calculate angle for tilt
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x) * 180 / math.pi
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Text overlays
    title_text = font.render("Generic Bobsled 1: Standard Racer", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4m | Weight: 200kg | Capacity: 4 | Speed Boost: +10 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Basic sled auto-called to track for balanced racing", True, WHITE)
    screen.blit(desc_text, (10, SCREEN_HEIGHT - 50))

def main():
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        draw_scene()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
