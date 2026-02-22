import pygame
import sys
import math
import random  # For bio-feedback, vision blurs, and hallucinations

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
SYNAPTIC_RED = (255, 0, 0, 128)  # Semi-transparent for firestorms
THOUGHT_BLUE = (0, 0, 255, 64)  # For thought fragments
DOPPEL_GRAY = (150, 150, 150, 128)  # For doppelgangers
BLUR_WHITE = (255, 255, 255, 32)  # For vision blurs

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge Course 15: Neural Overload")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# For animation (bio-feedback, vision blurs, path hallucinations, pulses)
feedback_timer = 0

def draw_track():
    global feedback_timer
    feedback_timer += 1
    # Draw background - throbbing neural core with synaptic firestorms
    screen.fill(DARK_BG)
    # Synaptic firestorms (random flashing areas)
    if feedback_timer % 15 < 5:  # Flash
        for _ in range(8):
            fx = random.randint(0, SCREEN_WIDTH)
            fy = random.randint(0, SCREEN_HEIGHT)
            fire_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.circle(fire_surface, SYNAPTIC_RED[:3], (50, 50), 50)
            screen.blit(fire_surface, (fx - 50, fy - 50))
    
    # Cascading thought fragments (falling text)
    for _ in range(10):
        tx = random.randint(50, SCREEN_WIDTH - 50)
        ty = (feedback_timer * 5 + random.randint(0, SCREEN_HEIGHT)) % (SCREEN_HEIGHT + 50) - 25
        thought_text = small_font.render("THOUGHT FRAGMENT", True, THOUGHT_BLUE[:3])
        screen.blit(thought_text, (tx, ty))
    
    # Hallucinatory visions of digital doppelgangers (faint figures along track)
    doppel_positions = [(200, 200), (600, 300), (300, 450)]
    for dx, dy in doppel_positions:
        doppel_surface = pygame.Surface((50, 100), pygame.SRCALPHA)
        pygame.draw.rect(doppel_surface, DOPPEL_GRAY[:3], (0, 0, 50, 100))
        screen.blit(doppel_surface, (dx + random.randint(-5, 5), dy + random.randint(-5, 5)))
    
    # Rogue consciousness echoes (whispering text overlays)
    if feedback_timer % 30 < 15:
        echo_text = small_font.render("Echo... Overload...", True, AI_RED)
        screen.blit(echo_text, (SCREEN_WIDTH // 2 - 100 + random.randint(-10, 10), 100))
        screen.blit(echo_text, (SCREEN_WIDTH // 2 - 100 + random.randint(-10, 10), 400))
    
    # Draw the track: 14 turns with near-vertical 30m plunge and sharp recovery
    track_width = 200
    start_x = (SCREEN_WIDTH - track_width) // 2
    points = []
    y_pos = 0
    pre_plunge_turns = 6  # Turns before plunge
    post_plunge_turns = 8  # After
    section_length = SCREEN_HEIGHT // (pre_plunge_turns + post_plunge_turns + 1)
    plunge_length = section_length * 2  # For 30m plunge
    
    # Pre-plunge turns
    current_x = start_x + track_width // 2
    for turn in range(pre_plunge_turns):
        direction = -1 if turn % 2 == 0 else 1
        radius = random.randint(80, 120)
        for i in range(0, section_length, 5):
            curve_x = current_x + direction * int(radius * math.sin(math.pi * i / section_length))
            halluc_offset = random.randint(-10, 10) if feedback_timer % 20 < 10 else 0  # Hallucination
            points.append((curve_x + halluc_offset, y_pos))
            y_pos += 10
        current_x = points[-1][0]
    
    # Near-vertical plunge (minimal horizontal, steep)
    plunge_start_y = y_pos
    for i in range(0, plunge_length, 3):  # Faster points for vertical feel
        plunge_x = current_x + random.randint(-5, 5)  # Slight wobble
        overload_offset = random.randint(-15, 15) if feedback_timer % 15 < 7 else 0  # Overload shake
        points.append((plunge_x + overload_offset, y_pos))
        y_pos += 10
    
    # Sharp recovery turn post-plunge
    recovery_direction = 1
    recovery_radius = 150
    for i in range(0, section_length, 5):
        curve_x = points[-1][0] + recovery_direction * int(recovery_radius * math.sin(math.pi * i / section_length))
        points.append((curve_x, y_pos))
        y_pos += 10
    current_x = points[-1][0]
    
    # Post-plunge turns
    for turn in range(post_plunge_turns - 1):  # -1 since recovery is one
        direction = -1 if turn % 2 == 0 else 1
        radius = random.randint(80, 120)
        for i in range(0, section_length, 5):
            curve_x = current_x + direction * int(radius * math.sin(math.pi * i / section_length))
            halluc_offset = random.randint(-10, 10) if feedback_timer % 20 < 10 else 0
            points.append((curve_x + halluc_offset, y_pos))
            y_pos += 10
        current_x = points[-1][0]
    
    # Fill to bottom
    while y_pos < SCREEN_HEIGHT:
        points.append((points[-1][0], y_pos))
        y_pos += 10
    
    # Draw the track surface with bio-neural circuits (pulsing veins)
    pygame.draw.lines(screen, GLOW_GREEN, False, points, track_width)
    if feedback_timer % 20 < 10:  # Pulse
        for point in points[::15]:
            pygame.draw.line(screen, SYNAPTIC_RED[:3], (point[0] - track_width // 2, point[1]), (point[0] + track_width // 2, point[1]), 3)
    
    # Illusory neural branches (fake paths during overload)
    if feedback_timer % 30 < 15:
        branch_start_idx = random.randint(100, len(points) - 100)
        branch_points = []
        branch_y = points[branch_start_idx][1]
        branch_x = points[branch_start_idx][0] + random.choice([-100, 100])
        for i in range(0, 100, 10):
            branch_x += random.randint(-20, 20)
            branch_points.append((branch_x, branch_y + i))
        pygame.draw.lines(screen, DOPPEL_GRAY[:3], False, branch_points, track_width // 2)
    
    # Draw consciousness uplink launch platform at top
    pygame.draw.rect(screen, NEON_PINK, (start_x - 50, 0, track_width + 100, 50), 5)
    # Flickering mind-link interfaces (small circles)
    for ix in range(start_x, start_x + track_width, 50):
        color = ENERGY_YELLOW if feedback_timer % 10 < 5 else HOLO_PURPLE
        pygame.draw.circle(screen, color, (ix, 25), 15)
    
    # Simulated bio-feedback vision blurs
    if feedback_timer % 40 < 10:  # Brief blur
        blur_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        blur_surface.fill(BLUR_WHITE)
        screen.blit(blur_surface, (0, 0))
    
    # Text overlays for theme
    title_text = font.render("Neural Overload", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = font.render("Length: 1700m | Drop: 160m | Turns: 14 | Max Speed: 125 km/h", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 30))
    
    desc_text = font.render("Elite plunge in neural highways network", True, WHITE)
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
