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
MERLIN_PURPLE = (128, 0, 128, 200)  # Semi-transparent magic hull
RUNE_GOLD = (255, 215, 0, 180)
MANA_BLUE = (0, 128, 255, 64)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Ultra Premium Bobsled 26: Merlin's Apex ($49.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)
rune_font = pygame.font.SysFont('arial', 14, bold=True)  # Sim rune

# Bobsled parameters
SLED_LENGTH = 137  # Pixels for visualization (supreme size)
SLED_WIDTH = 55
SLED_COLOR = MERLIN_PURPLE

# Rune pulses and mana particles
mana_timer = 0
mana_particles = []

def add_mana_particles(x, y):
    for _ in range(10):
        mana_particles.append([x + random.randint(-SLED_LENGTH // 2, SLED_LENGTH // 2), y + random.randint(-SLED_WIDTH // 2, SLED_WIDTH // 2), random.randint(3, 7), random.randint(80, 150), MANA_BLUE])

def update_mana_particles():
    global mana_timer
    mana_timer += 1
    for p in mana_particles[:]:
        p[0] += math.cos(mana_timer / 10 + p[0]) * 1  # Magical flow
        p[1] += math.sin(mana_timer / 10 + p[1]) * 1
        p[4] = list(p[4])
        p[4][3] -= 2  # Slow fade
        if p[4][3] <= 0:
            mana_particles.remove(p)

# Track simulation for auto-call (full mixed path for supreme demo)
track_points = []
start_x = SCREEN_WIDTH // 2
y_pos = 0
for i in range(0, SCREEN_HEIGHT, 10):
    curve_x = start_x + int(120 * math.sin(2.5 * math.pi * i / SCREEN_HEIGHT)) + random.randint(-25, 25)  # All-feature mix
    track_points.append((curve_x, i))

def draw_bobsled(pos_x, pos_y, angle=0):
    # Sorcerous hull
    hull_surf = pygame.Surface((SLED_LENGTH, SLED_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(hull_surf, SLED_COLOR[:3], (0, 0, SLED_LENGTH, SLED_WIDTH))
    screen.blit(hull_surf, (pos_x - SLED_LENGTH // 2, pos_y - SLED_WIDTH // 2))
    
    # Rune engravings (pulsing)
    rune_alpha = 180 + int(75 * math.sin(mana_timer / 10))
    rune_color = (RUNE_GOLD[0], RUNE_GOLD[1], RUNE_GOLD[2], rune_alpha)
    rune_text = rune_font.render("ᚱᚢᚾᛖ", True, rune_color[:3])  # Sim rune script
    screen.blit(rune_text, (pos_x - 30, pos_y - 10))
    
    # Runners
    for offset in [-10, 10]:
        pygame.draw.rect(screen, GLOW_GREEN, (pos_x - SLED_LENGTH // 2 + 15, pos_y + offset, SLED_LENGTH - 30, 5))
    
    # Add mana flow
    add_mana_particles(pos_x, pos_y)

def draw_scene():
    screen.fill(DARK_BG)
    # Draw mixed track
    pygame.draw.lines(screen, GLOW_GREEN, False, track_points, 100)  # Wide track
    
    # Auto-call bobsled to track
    sled_index = (pygame.time.get_ticks() // 13) % len(track_points)  # Magical speed
    sled_x, sled_y = track_points[sled_index]
    # Angle
    if sled_index < len(track_points) - 1:
        next_x, next_y = track_points[sled_index + 1]
        angle = math.atan2(next_y - sled_y, next_x - sled_x)
    else:
        angle = 0
    draw_bobsled(sled_x, sled_y, angle)
    
    # Update mana
    update_mana_particles()
    for p in mana_particles:
        pygame.draw.circle(screen, p[4][:3], (int(p[0]), int(p[1])), p[2])
    
    # Text overlays
    title_text = font.render("Ultra Premium Bobsled 26: Merlin's Apex", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    stats_text = small_font.render("Length: 5.5m | Weight: 280kg | Capacity: 4 | Boost: Supreme +25 km/h all", True, WHITE)
    screen.blit(stats_text, (10, SCREEN_HEIGHT - 60))
    
    price_text = small_font.render("LOCKED - $49.99 USD Unlock + 5 Hoodie Codes", True, GOLD)
    screen.blit(price_text, (10, SCREEN_HEIGHT - 40))
    
    desc_text = small_font.render("Cyber-magic fusion supreme stats | Auto-called to tracks", True, WHITE)
    screen.blit(desc_text, (10, SCREEN_HEIGHT - 20))
    
    coupon_text = small_font.render("Email purchase screenshot to stakeme10000@gmail.com for codes", True, GOLD)
    screen.blit(coupon_text, (10, SCREEN_HEIGHT - 80))

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
