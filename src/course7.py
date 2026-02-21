import pygame
import sys
import math
import random  # For market volatility simulations and glitches

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
CURRENCY_GREEN = (0, 255, 100, 128)  # Semi-transparent for holograms
ELECTRIC_BLUE = (0, 191, 255)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 7: Cyber-Bank Helix")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)
ticker_font = pygame.font.SysFont('couriernew', 10)

# For animation (market volatility flares and data glitches)
volatility_timer = 0

def draw_track():
    global volatility_timer
    volatility_timer += 1
    # Draw background - electrified atmosphere with gradient
    screen.fill(DARK_BG)
    for y in range(0, SCREEN_HEIGHT, 5):
        alpha = int(40 * math.sin(volatility_timer / 20 + y / 50))  # Wavy effect
        pygame.draw.line(screen, (0, 0, alpha + 50), (0, y), (SCREEN_WIDTH, y), 1)
    
    # Draw corporate spire (central helix structure as stacked circles/ellipses)
    for y in range(100, 500, 50):
        radius = 100 + int(50 * math.sin(y / 100))
        pygame.draw.ellipse(screen, NEON_BLUE, (SCREEN_WIDTH // 2 - radius // 2, y, radius, 30), 2)
    
    # Draw cascading digital stock tickers (moving text)
    ticker_y_positions = [50, 150, 250, 350, 450]
    for ty in ticker_y_positions:
        ticker_text = ticker_font.render("BTC: $45k ▼ ETH: $3k ▲ NEO: $120k ► Crash Imminent!", True, CURRENCY_GREEN[:3])
        tx = (volatility_timer % (SCREEN_WIDTH + ticker_text.get_width())) - ticker_text.get_width()
        screen.blit(ticker_text, (tx, ty))
    
    # Draw holographic market crashes (flashing polygons)
    if volatility_timer % 30 < 15:  # Blink effect
        crash_points = [(200, 200), (250, 150), (300, 200), (250, 250)]
        pygame.draw.polygon(screen, AI_RED, crash_points, 0)
        crash_points2 = [(500, 300), (550, 250), (600, 300), (550, 350)]
        pygame.draw.polygon(screen, AI_RED, crash_points2, 0)
    
    # Draw the track: helical descent with 5 high-banked turns (spiral pattern)
    track_width = 200
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    points = []
    angle_step = 2 * math.pi / (SCREEN_HEIGHT / 10)  # For spiral
    radius = 150
    y_pos = 0
    turn_count = 0
    for i in range(0, SCREEN_HEIGHT, 10):
        angle = i * angle_step * 1.5  # Adjust for 5 turns (approx 5 full rotations)
        x = center_x + int(radius * math.cos(angle)) + random.randint(-3, 3) if volatility_timer % 5 == 0 else center_x + int(radius * math.cos(angle))
        y = y_pos + int(20 * math.sin(angle / 5))  # Add banking undulation
        points.append((x, y))
        y_pos += 10
        radius -= 0.2  # Inward spiral for helix effect
    
    # Draw the track surface with magnetic lev rails (parallel lines)
    pygame.draw.lines(screen, GLOW_GREEN, False, points, track_width)
    # Inner rails
    inner_points = [(p[0] - track_width // 4 + random.randint(-2, 2), p[1]) for p in points]
    pygame.draw.lines(screen, ELECTRIC_BLUE, False, inner_points, 2)
    outer_points = [(p[0] + track_width // 4 + random.randint(-2, 2), p[1]) for p in points]
    pygame.draw.lines(screen, ELECTRIC_BLUE, False, outer_points, 2)
    
    # Add data streams (lines along track)
    for point in points[::10]:
        pygame.draw.line(screen, HOLO_PURPLE, (point[0] - track_width // 2, point[1]), (point[0] + track_width // 2, point[1]), 1)
    
    # Draw penthouse executive launch platform at top
    pygame.draw.rect(screen, NEON_PINK, (center_x - 100, 0, 200, 50), 5)
    # Overlooking trading floors (small rects below)
    for fx in range(center_x - 150, center_x + 150, 50):
        pygame.draw.rect(screen, ENERGY_YELLOW, (fx, 50, 40, 20), 1)
    
    # Rogue trading bots (small circles with lines)
    for _ in range(3):
        bx = 150 + _ * 200
        by = 200 + _ * 100
        pygame.draw.circle(screen, AI_RED, (bx, by), 15)
        pygame.draw.line(screen, AI_RED, (bx, by), (bx + random.randint(-50, 50), by + random.randint(-50, 50)), 1)
    
    # Volatile currency holograms (text with glitch)
    if volatility_timer % 20 < 10:
        holo_text = small_font.render("$CRASH 404", True, CURRENCY_GREEN[:3])
        screen.blit(holo_text, (300 + random.randint(-5, 5), 400 + random.randint(-5, 5)))
        screen.blit(holo_text, (500 + random.randint(-5, 5), 200 + random.randint(-5, 5)))
    
    # Text overlays for theme
    title_text = font.render("Cyber-Bank Helix", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 900m | Drop: 80m | Turns: 5 | Max Speed: 85 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Intermediate banks in corporate financial spire", True, WHITE)
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
