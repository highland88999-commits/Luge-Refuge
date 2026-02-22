import pygame
import sys
import math
import random  # For neural overloads, glitches, and shifting decoys

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
CODE_GREEN = (0, 200, 0, 128)  # Semi-transparent for code matrices
PHANTOM_GRAY = (100, 100, 100, 64)  # For holographic phantoms
FIREWALL_ORANGE = (255, 69, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 11: Data Labyrinth Vortex")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)
code_font = pygame.font.SysFont('couriernew', 10)

# For animation (neural overloads, glitches, shifting decoys)
overload_timer = 0

def draw_track():
    global overload_timer
    overload_timer += 1
    # Draw background - void of quantum firewalls with server hum (gradient)
    screen.fill(DARK_BG)
    for y in range(0, SCREEN_HEIGHT, 10):
        alpha = int(50 * math.sin(overload_timer / 30 + y / 50))  # Wavy hum effect
        pygame.draw.line(screen, (FIREWALL_ORANGE[0], FIREWALL_ORANGE[1], FIREWALL_ORANGE[2] + alpha), (0, y), (SCREEN_WIDTH, y), 1)
    
    # Draw walls of encrypted code matrices (grids of binary text)
    for x in range(50, SCREEN_WIDTH - 50, 100):
        for y in range(50, SCREEN_HEIGHT - 50, 50):
            matrix_surface = pygame.Surface((80, 40), pygame.SRCALPHA)
            code_text = code_font.render("101010 010101", True, CODE_GREEN[:3])
            matrix_surface.blit(code_text, (0, 0))
            code_text2 = code_font.render("ENCRYPTED", True, CODE_GREEN[:3])
            matrix_surface.blit(code_text2, (0, 15))
            screen.blit(matrix_surface, (x + random.randint(-2, 2) if overload_timer % 10 < 5 else x, y))
    
    # Draw surging information torrents (vertical lines with moving text)
    for x in [150, 650]:
        offset = (overload_timer % 60) - 30  # Surging up/down
        for y in range(0, SCREEN_HEIGHT, 60):
            pygame.draw.line(screen, ENERGY_YELLOW, (x, y + offset), (x, y + offset + 50), 3)
            torrent_text = small_font.render("DATA TORRENT", True, ENERGY_YELLOW)
            screen.blit(torrent_text, (x - 40, y + offset + 10))
    
    # Draw holographic data phantoms (deceptive paths, flickering fake tracks)
    if overload_timer % 25 < 12:  # Flicker
        fake_points = []
        fake_start_x = SCREEN_WIDTH // 4
        fake_y = 100
        for i in range(0, 300, 10):
            fake_x = fake_start_x + int(100 * math.sin(2 * math.pi * i / 100)) + random.randint(-10, 10)
            fake_points.append((fake_x, fake_y))
            fake_y += 10
        pygame.draw.lines(screen, PHANTOM_GRAY[:3], False, fake_points, 100)  # Wide fake track
        # Another decoy
        fake_points2 = []
        fake_start_x2 = SCREEN_WIDTH * 3 // 4
        fake_y2 = 300
        for i in range(0, 200, 10):
            fake_x2 = fake_start_x2 - int(80 * math.cos(2 * math.pi * i / 80)) + random.randint(-10, 10)
            fake_points2.append((fake_x2, fake_y2))
            fake_y2 += 10
        pygame.draw.lines(screen, PHANTOM_GRAY[:3], False, fake_points2, 100)
    
    # Draw the track: Dense maze-like 10 turns with variable radii
    track_width = 200
    start_x = (SCREEN_WIDTH - track_width) // 2
    points = []
    y_pos = 0
    turn_lengths = [SCREEN_HEIGHT // 12] * 10  # Roughly equal sections for 10 turns
    radii = [random.randint(80, 150) for _ in range(10)]  # Variable radii
    
    for turn in range(10):
        direction = -1 if turn % 2 == 0 else 1
        radius = radii[turn]
        section_length = turn_lengths[turn]
        for i in range(0, section_length, 5):
            curve_x = (points[-1][0] if points else start_x + track_width // 2) + direction * int(radius * math.sin(math.pi * i / section_length))
            glitch_offset = random.randint(-8, 8) if overload_timer % 15 < 7 else 0  # Neural glitch
            points.append((curve_x + glitch_offset, y_pos))
            y_pos += 10
    
    # Adjust for total height if needed
    if y_pos < SCREEN_HEIGHT:
        for i in range(y_pos, SCREEN_HEIGHT, 10):
            points.append((points[-1][0], i))
    
    # Draw the track surface with neural feedback loops (pulsing lines)
    pygame.draw.lines(screen, GLOW_GREEN, False, points, track_width)
    if overload_timer % 20 < 10:  # Pulse
        for point in points[::10]:
            pygame.draw.circle(screen, HOLO_PURPLE, point, 10 + random.randint(0, 5))
    
    # Draw secure data vault entry platform at top
    pygame.draw.rect(screen, NEON_PINK, (start_x - 50, 0, track_width + 100, 50), 5)
    # Virtual sentinels (circles guarding)
    pygame.draw.circle(screen, AI_RED, (start_x - 80, 25), 20)
    pygame.draw.circle(screen, AI_RED, (start_x + track_width + 80, 25), 20)
    
    # Simulated neural overloads (screen-wide glitches)
    if overload_timer % 40 < 5:  # Brief full glitch
        glitch_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for _ in range(100):
            gx = random.randint(0, SCREEN_WIDTH)
            gy = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.line(glitch_surface, STATIC_GRAY[:3], (gx, gy), (gx + random.randint(-20, 20), gy), 2)
        screen.blit(glitch_surface, (0, 0))
    
    # Text overlays for theme
    title_text = font.render("Data Labyrinth Vortex", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 1300m | Drop: 120m | Turns: 10 | Max Speed: 105 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Expert beginner maze in data vaults core", True, WHITE)
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
