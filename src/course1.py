import pygame
import sys

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

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 1: Neon Descent Alley")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)

def draw_track():
    # Draw background - dark city night
    screen.fill(DARK_BG)
    
    # Draw holographic billboards (rectangles with neon borders)
    pygame.draw.rect(screen, NEON_BLUE, (50, 100, 100, 400), 2)
    pygame.draw.rect(screen, NEON_PINK, (650, 100, 100, 400), 2)
    
    # Draw the straight track - glowing ice-like surface
    track_width = 200
    track_start_x = (SCREEN_WIDTH - track_width) // 2
    pygame.draw.rect(screen, GLOW_GREEN, (track_start_x, 0, track_width, SCREEN_HEIGHT))
    
    # Add pulsing LED effects (simple lines)
    for y in range(0, SCREEN_HEIGHT, 20):
        pygame.draw.line(screen, NEON_BLUE, (track_start_x, y), (track_start_x + track_width, y), 1)
    
    # Draw rooftop launch pad at top
    pygame.draw.rect(screen, NEON_PINK, (track_start_x - 50, 0, track_width + 100, 50), 5)
    
    # Text overlays for theme
    title_text = font.render("Neon Descent Alley", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 300m | Drop: 20m | Turns: 0 | Max Speed: 50 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Beginner straight slope in cyberpunk megacity", True, WHITE)
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
