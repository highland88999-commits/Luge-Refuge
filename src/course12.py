import pygame
import sys
import math
import random  # For gale bursts, track sway, and debris

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
WIND_GRAY = (150, 150, 150, 128)  # Semi-transparent for wind effects
DEBRIS_BROWN = (139, 69, 19)
TURBINE_SILVER = (192, 192, 192)
RUST_ORANGE = (204, 85, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 12: Aero-Tunnel Gale")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# For animation (gale bursts, track sway, visual blurs, debris)
gale_timer = 0

def draw_track():
    global gale_timer
    gale_timer += 1
    # Draw background - enclosed tunnel with wind-swept haze
    screen.fill(DARK_BG)
    # Tunnel walls (vertical gradients)
    for x in [50, 750]:
        pygame.draw.rect(screen, RUST_ORANGE, (x, 0, 20, SCREEN_HEIGHT), 0)
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(screen, TURBINE_SILVER, (x, y), (x + 20, y), 2)
    
    # Rusted fan blades (rotating circles with blades)
    fan_positions = [(200, 150), (600, 350), (400, 500)]
    for fx, fy in fan_positions:
        angle = gale_timer * 5 % 360  # Rotating
        pygame.draw.circle(screen, TURBINE_SILVER, (fx, fy), 50, 2)
        for b in range(4):
            blade_angle = angle + b * 90
            end_x = fx + int(50 * math.cos(math.radians(blade_angle)))
            end_y = fy + int(50 * math.sin(math.radians(blade_angle)))
            pygame.draw.line(screen, TURBINE_SILVER, (fx, fy), (end_x, end_y), 5)
    
    # Swirling debris holograms (moving particles)
    debris_positions = []
    for _ in range(20):
        dx = random.randint(0, SCREEN_WIDTH)
        dy = (gale_timer * 10 + random.randint(0, SCREEN_HEIGHT)) % (SCREEN_HEIGHT + 100) - 50
        sway = int(20 * math.sin(gale_timer / 10 + dx / 50))  # Wind sway
        debris_positions.append((dx + sway, dy))
        pygame.draw.circle(screen, DEBRIS_BROWN, (dx + sway, dy), random.randint(3, 8))
    
    # Directional air currents (semi-transparent arrows/lines)
    wind_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    if gale_timer % 30 < 15:  # Burst effect
        for y in range(0, SCREEN_HEIGHT, 20):
            for x in range(0, SCREEN_WIDTH, 50):
                pygame.draw.line(wind_surface, WIND_GRAY[:3], (x, y), (x + 40 + random.randint(-10, 10), y), 2)
    screen.blit(wind_surface, (0, 0))
    
    # Rogue wind spirits (ethereal projections, whispering text)
    spirit_positions = [(300, 200), (500, 400)]
    for sx, sy in spirit_positions:
        spirit_surface = pygame.Surface((100, 50), pygame.SRCALPHA)
        pygame.draw.ellipse(spirit_surface, (HOLO_PURPLE + (128,)), (0, 0, 100, 50))
        whisper_text = small_font.render("Turn... Now...", True, WHITE)
        spirit_surface.blit(whisper_text, (10, 15))
        sway_x = sx + int(15 * math.sin(gale_timer / 15))
        sway_y = sy + int(10 * math.cos(gale_timer / 15))
        screen.blit(spirit_surface, (sway_x, sway_y))
    
    # Draw the track: 11 turns in enclosed tunnel, with sway
    track_width = 200
    start_x = (SCREEN_WIDTH - track_width) // 2
    points = []
    y_pos = 0
    turn_lengths = [SCREEN_HEIGHT // 13] * 11  # Approx equal for 11 turns
    directions = [(-1 if i % 2 == 0 else 1) for i in range(11)]
    
    for turn in range(11):
        direction = directions[turn]
        section_length = turn_lengths[turn] + random.randint(-10, 10)  # Variable
        radius = random.randint(100, 150)
        for i in range(0, section_length, 5):
            curve_x = (points[-1][0] if points else start_x + track_width // 2) + direction * int(radius * math.sin(math.pi * i / section_length))
            sway_offset = int(10 * math.sin(gale_timer / 20 + y_pos / 50)) if gale_timer % 40 < 20 else 0  # Gale sway
            points.append((curve_x + sway_offset, y_pos))
            y_pos += 10
    
    # Ensure full height
    while y_pos < SCREEN_HEIGHT:
        points.append((points[-1][0], y_pos))
        y_pos += 10
    
    # Draw the track surface
    pygame.draw.lines(screen, GLOW_GREEN, False, points, track_width)
    
    # Visual blurs (semi-transparent overlays during bursts)
    if gale_timer % 30 < 10:
        blur_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        blur_surface.fill((200, 200, 200, 20))  # Light blur
        screen.blit(blur_surface, (0, 0))
    
    # Draw ventilation shaft entry platform at top
    pygame.draw.rect(screen, NEON_PINK, (start_x - 50, 0, track_width + 100, 50), 5)
    # Spinning turbine guardians (small fans)
    for gx in [start_x - 100, start_x + track_width + 100]:
        pygame.draw.circle(screen, TURBINE_SILVER, (gx, 25), 30, 2)
        for b in range(3):
            blade_angle = gale_timer * 10 % 360 + b * 120
            end_x = gx + int(30 * math.cos(math.radians(blade_angle)))
            end_y = 25 + int(30 * math.sin(math.radians(blade_angle)))
            pygame.draw.line(screen, TURBINE_SILVER, (gx, 25), (end_x, end_y), 3)
    
    # Text overlays for theme
    title_text = font.render("Aero-Tunnel Gale", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 1400m | Drop: 130m | Turns: 11 | Max Speed: 110 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Expert wind tunnels in megacity undergrid", True, WHITE)
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
