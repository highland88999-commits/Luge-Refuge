import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors for cyberpunk aesthetic
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
DARK_BG = (10, 10, 20)
AI_STEEL = (80, 80, 80, 200)  # Semi-transparent metal
OPTIC_RED = (255, 0, 0, 180)
LASER_BLUE = (0, 100, 255, 128)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 8: AI Overlord ($2.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 110  # Pixels for visualization
SLED_WIDTH = 45
SLED_COLOR = AI_STEEL

# Tentacle and laser scan
tentacle_timer = 0
laser_beams = []

def add_laser_beams(x, y):
    for _ in range(2):
        laser_beams.append([x, y, random.randint(50, 150), random.randint(30, 60), LASER_BLUE])

def update_laser_beams():
    global tentacle_timer
    tentacle_timer += 1
    for b in laser_beams[:]:
        b[2] -= 5  # Shorten beam
        b[4] = list(b[4])
        b[4][3] -= 5  # Fade
        if b[4][3] <= 0:
            laser_beams.remove(b)

# Track simulation for auto-call (chicane-heavy path for turning demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(110 * math.sin(4 * math.pi * i / SCREEN_HEIGHT))  # Zigzag chicanes
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Sentient chassis
    chassis_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(chassis_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(chassis_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Extendable tentacles (arms)
    arm_length = 30 + int(20 * math.sin(tentacle_timer / 8))
    for side in [-1, 1]:
        arm_start_x = pos_x + side * (SLED_LENGTH // 4)
        arm_start_y = pos_y
        arm_end_x = arm_start_x + side * arm_length
        arm_end_y = arm_start_y + math.sin(tentacle_timer / 10) * 10
        pygame.draw.line(screen, NEON_PINK, (arm_start_x, arm_start_y), (arm_end_x, arm_end_y), 6)
    
    # Optic sensors (eyes)
    for eye in [-15, 15]:
        pygame.draw.circle(screen, OPTIC_RED[:3], (pos_x + eye, pos_y - 10), 8)
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add laser scans
    if tentacle_timer % 15 == 0:
        add_laser_beams(pos_x, pos_y - 20)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw chicane track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 17) % len(track_points)  # Precise speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update lasers
    update_laser_beams()
    for b in laser_beams:
        end_x = b[0]
        end_y = b[1] - b[2]
        pygame.draw.line(screen, b[4][:3], (b[0], b[1]), (end_x, end_y), 2)
    
    # Text overlays
    title_text = font.render("Premium Bobsled 8: AI Overlord", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 4.6m | Weight: 225kg | Capacity: 4 | Boost: +12 km/h chicanes", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 50))
    
    price_text = small_font.render("LOCKED - $2.99 USD Unlock", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = small_font.render("Adaptive turns +12 km/h chicanes | Auto-called to tracks", True, WHITE)
    screen.blit(desc_text, (10, SCREEN_HEIGHT - 70))

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
